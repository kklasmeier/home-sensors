from fastapi import APIRouter, HTTPException

from api.database import get_connection
from api.serialize import php_json_row, php_json_rows, php_json_value

router = APIRouter(prefix="/sensors", tags=["Sensors"])

LOCATIONS = ["Attic", "Garage", "Inside", "Outside", "HVAC"]
SENSORS = ["temperature_f", "heat_index_f", "humidity_pct", "pressure_inHg"]
INTERVALS = ["HOUR", "DAY", "WEEK", "MONTH", "YEAR"]

STATUS_SQL = """
SELECT location, latest_reading, diff_seconds FROM (
  SELECT location, MAX(reading_dttm) AS latest_reading,
         TIMESTAMPDIFF(SECOND, MAX(reading_dttm), NOW()) AS diff_seconds
  FROM sensor_readings GROUP BY location
  UNION
  SELECT 'Garagedoor' AS location, MAX(reading_dttm) AS latest_reading,
         TIMESTAMPDIFF(SECOND, MAX(reading_dttm), NOW()) AS diff_seconds
  FROM sensor_readings_garage
  UNION
  SELECT 'SumpPump' AS location, MAX(reading_dttm) AS latest_reading,
         TIMESTAMPDIFF(SECOND, MAX(reading_dttm), NOW()) AS diff_seconds
  FROM sensor_readings_sump_pump
) AS statuses
"""

CHART_SQL = """
SELECT
    CONCAT(
        DATE_FORMAT(reading_dttm, '%Y-%m-%d %H:'),
        LPAD(FLOOR(DATE_FORMAT(reading_dttm, '%i')/2)*2, 2, '0'),
        ':00'
    ) AS reading_dttm,
    location,
    AVG(temperature_f) AS temperature_f,
    AVG(heat_index_f) AS heat_index_f,
    AVG(humidity_pct) AS humidity_pct,
    AVG(pressure_inHg) AS pressure_inHg
FROM sensor_readings
WHERE reading_dttm > DATE_SUB(NOW(), INTERVAL 24 HOUR)
  AND location = %s
GROUP BY location,
    CONCAT(
        DATE_FORMAT(reading_dttm, '%Y-%m-%d %H:'),
        LPAD(FLOOR(DATE_FORMAT(reading_dttm, '%i')/2)*2, 2, '0'),
        ':00'
    )
ORDER BY location, reading_dttm
"""


def _status_color(diff_seconds: int) -> str:
    if diff_seconds <= 180:
        return "Green"
    if diff_seconds <= 600:
        return "Yellow"
    return "Red"


def _summary_sql(interval: str, sensor: str, location: str) -> str:
    if interval == "HOUR":
        return (
            f"SELECT MAX({sensor}) as high, MIN({sensor}) as low "
            f"FROM sensor_readings "
            f"WHERE reading_dttm BETWEEN DATE_SUB(NOW(), INTERVAL 1 HOUR) AND NOW() "
            f"AND location = %s"
        )

    start_map = {
        "DAY": "DATE_SUB(CURDATE(), INTERVAL 1 DAY)",
        "WEEK": "DATE_SUB(CURDATE(), INTERVAL 1 WEEK)",
        "MONTH": "DATE_SUB(CURDATE(), INTERVAL 1 MONTH)",
        "YEAR": "DATE_SUB(CURDATE(), INTERVAL 1 YEAR)",
    }
    start_time = start_map[interval]
    sensor_high = f"max_{sensor}"
    sensor_low = f"min_{sensor}"
    return (
        f"SELECT `{sensor_high}` as high, `{sensor_low}` as low "
        f"FROM sensor_readings_summary "
        f"WHERE summary_date BETWEEN {start_time} AND CURDATE() AND location = %s "
        f"LIMIT 1"
    )


@router.get("/status")
def sensor_status():
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(STATUS_SQL)
        rows = cursor.fetchall()
        cursor.close()

    result = []
    for row in rows:
        diff_seconds = int(row["diff_seconds"])
        result.append(
            {
                "location": row["location"],
                "status": _status_color(diff_seconds),
                "diff_seconds": diff_seconds,
            }
        )
    return result


@router.get("/current")
def current_readings():
    readings: dict[str, dict | None] = {}
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        for location in LOCATIONS:
            cursor.execute(
                """
                SELECT temperature_f, heat_index_f, humidity_pct, pressure_inHg
                FROM sensor_readings
                WHERE location = %s
                ORDER BY reading_dttm DESC
                LIMIT 1
                """,
                (location,),
            )
            row = cursor.fetchone()
            readings[location] = php_json_row(row) if row else None
        cursor.close()
    return readings


@router.get("/{location}/charts")
def location_charts(location: str):
    if location not in LOCATIONS:
        raise HTTPException(status_code=404, detail="Unknown location")

    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(CHART_SQL, (location,))
        rows = cursor.fetchall()
        cursor.close()
    return php_json_rows(rows)


@router.get("/{location}/summary")
def location_summary(location: str):
    if location not in LOCATIONS:
        raise HTTPException(status_code=404, detail="Unknown location")

    results: dict[str, dict[str, str]] = {}
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        for sensor in SENSORS:
            results[sensor] = {}
            for interval in INTERVALS:
                sql = _summary_sql(interval, sensor, location)
                cursor.execute(sql, (location,))
                row = cursor.fetchone()
                if row and row["high"] is not None and row["low"] is not None:
                    high = php_json_value(row["high"])
                    low = php_json_value(row["low"])
                    results[sensor][interval] = f"{high} / {low}"
                else:
                    results[sensor][interval] = "N/A"
        cursor.close()
    return results
