from datetime import datetime

from fastapi import APIRouter

from api.database import get_connection
from api.serialize import php_json_row

router = APIRouter(prefix="/sump-pump", tags=["Sump Pump"])

CHART_SQL = """
SELECT
    CONCAT(
        DATE_FORMAT(reading_dttm, '%Y-%m-%d %H:'),
        LPAD(FLOOR(DATE_FORMAT(reading_dttm, '%i')/2)*2, 2, '0'),
        ':00'
    ) AS reading_dttm,
    AVG(water_level) AS water_level
FROM sensor_readings_sump_pump
WHERE reading_dttm > DATE_SUB(NOW(), INTERVAL 100 HOUR)
GROUP BY CONCAT(
    DATE_FORMAT(reading_dttm, '%Y-%m-%d %H:'),
    LPAD(FLOOR(DATE_FORMAT(reading_dttm, '%i')/2)*2, 2, '0'),
    ':00'
)
ORDER BY reading_dttm
"""


@router.get(
    "/charts",
    summary="Sump pump water level trend",
    description=(
        "Returns 2-minute averaged water level readings for roughly the last 100 hours. "
        "Used for the sump pump line chart on the dashboard."
    ),
)
def sump_pump_charts():
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(CHART_SQL)
        rows = cursor.fetchall()
        cursor.close()
    return [php_json_row(row) for row in rows]


@router.get(
    "/cycles",
    summary="Daily sump pump cycle counts",
    description=(
        "Calls stored procedure `CountRapidFalls` and returns the number of pump cycles per day."
    ),
)
def sump_pump_cycles():
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.callproc("CountRapidFalls")
        rows = []
        for result in cursor.stored_results():
            rows.extend(result.fetchall())
        cursor.close()

    return [
        {
            "reading_date": row["reading_date"].strftime("%Y-%m-%d")
            if isinstance(row.get("reading_date"), datetime)
            else row.get("reading_date"),
            "num_cycles": str(row["num_cycles"]),
        }
        for row in rows
    ]
