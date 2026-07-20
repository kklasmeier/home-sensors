from datetime import date, datetime

from fastapi import APIRouter

from api.database import get_connection

router = APIRouter(prefix="/hvac", tags=["HVAC"])


def _serialize_row(row: dict) -> dict:
    result = {}
    for key, value in row.items():
        if isinstance(value, datetime):
            result[key] = value.strftime("%Y-%m-%d")
        elif isinstance(value, date):
            result[key] = value.strftime("%Y-%m-%d")
        else:
            result[key] = value
    return result


@router.get("/cycles")
def hvac_cycles():
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.callproc("FindCyclesByDate")
        rows = []
        for result in cursor.stored_results():
            rows.extend(result.fetchall())
        cursor.close()
    return [_serialize_row(row) for row in rows]
