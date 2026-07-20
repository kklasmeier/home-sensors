from datetime import datetime


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Home Sensors API"
    assert body["docs"] == "/docs"


def test_sensor_status_shape(client, mock_db_connection):
    mock_db_connection(
        fetchall=[
            {"location": "Garage", "diff_seconds": 45},
            {"location": "Attic", "diff_seconds": 900},
        ]
    )
    response = client.get("/api/v1/sensors/status")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0] == {"location": "Garage", "status": "Green", "diff_seconds": 45}
    assert data[1] == {"location": "Attic", "status": "Red", "diff_seconds": 900}


def test_current_readings_shape(client, mock_db_connection):
    cursor = mock_db_connection(
        fetchone={
            "temperature_f": "72.5",
            "heat_index_f": "74.0",
            "humidity_pct": "45.0",
            "pressure_inHg": "30.12",
        }
    )
    response = client.get("/api/v1/sensors/current")
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {"Attic", "Garage", "Inside", "Outside", "HVAC"}
    assert data["Garage"]["temperature_f"] == "72.5"
    assert cursor.execute.call_count == 5


def test_unknown_location_charts(client):
    response = client.get("/api/v1/sensors/Unknown/charts")
    assert response.status_code == 404


def test_garage_status_shape(client, mock_db_connection):
    now = datetime(2026, 7, 19, 21, 0, 0)
    earlier = datetime(2026, 7, 19, 18, 0, 0)
    mock_db_connection(
        fetchone_sequence=[
            {"2Door": "UP"},
            {"2Door": "UP", "reading_dttm": now},
            {"reading_dttm": earlier},
            {"1Door": "DOWN"},
            {"1Door": "DOWN", "reading_dttm": now},
            {"reading_dttm": earlier},
        ]
    )
    response = client.get("/api/v1/garage/status")
    assert response.status_code == 200
    data = response.json()
    assert "doors" in data
    assert len(data["doors"]) == 2
    assert data["doors"][0]["label"] == "Main Garage Door"


def test_openapi_docs(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    paths = schema["paths"]
    assert "/api/v1/sensors/status" in paths
    assert "/api/v1/garage/status" in paths
    assert "/api/v1/logs/collect" in paths
