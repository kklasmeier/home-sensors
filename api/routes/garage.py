from datetime import datetime

from fastapi import APIRouter

from api.database import get_connection

router = APIRouter(prefix="/garage", tags=["Garage"])

DOORS = {
    "Main Garage Door": "2Door",
    "3rd Car Door": "1Door",
}


def _calculate_duration(conn, column: str) -> str:
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        f"SELECT reading_dttm, {column} FROM sensor_readings_garage "
        f"ORDER BY reading_dttm DESC LIMIT 1"
    )
    current = cursor.fetchone()
    if not current:
        cursor.close()
        return "0 hours, 0 minutes"

    current_state = current[column]
    current_ts = current["reading_dttm"]

    cursor.execute(
        f"SELECT reading_dttm FROM sensor_readings_garage "
        f"WHERE {column} != %s ORDER BY reading_dttm DESC LIMIT 1",
        (current_state,),
    )
    previous = cursor.fetchone()
    cursor.close()

    if not previous:
        return "0 hours, 0 minutes"

    delta = int(
        (current_ts - previous["reading_dttm"]).total_seconds()
        if isinstance(current_ts, datetime)
        else 0
    )
    hours = delta // 3600
    minutes = (delta // 60) % 60
    return f"{hours} hours, {minutes} minutes"


@router.get("/status")
def garage_status():
    doors = []
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        for label, column in DOORS.items():
            cursor.execute(
                f"SELECT {column} FROM sensor_readings_garage "
                f"ORDER BY reading_dttm DESC LIMIT 1"
            )
            row = cursor.fetchone()
            status = row[column] if row else "DOWN"
            image = "GarageOpen.jpg" if status == "UP" else "GarageClosed.jpg"
            duration = _calculate_duration(conn, column)
            doors.append(
                {
                    "label": label,
                    "column": column,
                    "status": status,
                    "image": image,
                    "duration": duration,
                }
            )
        cursor.close()
    return {"doors": doors}


@router.get("/charts")
def garage_charts():
    sql = """
    SELECT reading_dttm, 2Door AS mainGarageDoor, 1Door AS thirdCarDoor
    FROM sensor_readings_garage
    WHERE reading_dttm > DATE_SUB(NOW(), INTERVAL 1 DAY)
    ORDER BY reading_dttm
    """
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()

    data = []
    for row in rows:
        data.append(
            {
                "reading_dttm": row["reading_dttm"].strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(row["reading_dttm"], datetime)
                else row["reading_dttm"],
                "mainGarageDoor": 1 if row["mainGarageDoor"] == "UP" else 0,
                "thirdCarDoor": 1 if row["thirdCarDoor"] == "UP" else 0,
            }
        )
    return data
