"""OpenAPI descriptions for /docs and /redoc."""

API_DESCRIPTION = """
Read-only HTTP API for home sensor data in MariaDB `homedata`.

**Data flow:** Python collectors poll Pico/ESP nodes about every 60 seconds and insert readings. This API serves that data to the dashboard and other clients on the LAN.

**Base path:** `/api/v1`

**Environment locations:** `Attic`, `Garage`, `Inside`, `Outside`, `HVAC`

**Other sources:** garage doors and sump pump (status via `/sensors/status`; detail under `/garage` and `/sump-pump`)

**Authentication:** None in v1 (LAN-trust only)

**Methods:** GET only — no endpoints modify the database
""".strip()

OPENAPI_TAGS = [
    {
        "name": "Sensors",
        "description": (
            "Environment sensor freshness, current readings, 24-hour chart series, "
            "and high/low summaries for Attic, Garage, Inside, Outside, and HVAC."
        ),
    },
    {
        "name": "Garage",
        "description": "Main and 3rd-car garage door state, duration in current state, and 24-hour history.",
    },
    {
        "name": "Sump Pump",
        "description": "Basement sump pump water level trends and daily cycle counts.",
    },
    {
        "name": "HVAC",
        "description": "Daily HVAC cycle counts from stored procedure `FindCyclesByDate`.",
    },
    {
        "name": "Logs",
        "description": "Collector log file used to diagnose ingest errors.",
    },
]
