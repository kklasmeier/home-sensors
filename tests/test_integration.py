"""Live integration tests — run on PiSensors with services up.

Skip by default; enable with: RUN_INTEGRATION=1 pytest -m integration
"""

import os

import httpx
import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_INTEGRATION") != "1",
    reason="Set RUN_INTEGRATION=1 to run live PiSensors checks",
)

API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8090")


@pytest.fixture
def api():
    with httpx.Client(base_url=API_BASE, timeout=30.0) as client:
        yield client


@pytest.mark.integration
def test_api_health(api):
    response = api.get("/")
    assert response.status_code == 200


@pytest.mark.integration
def test_sensor_status_live(api):
    response = api.get("/api/v1/sensors/status")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    for item in data:
        assert item["status"] in ("Green", "Yellow", "Red")
        assert "location" in item
        assert "diff_seconds" in item


@pytest.mark.integration
def test_all_v1_endpoints_respond(api):
    endpoints = [
        "/api/v1/sensors/status",
        "/api/v1/sensors/current",
        "/api/v1/sensors/Garage/charts",
        "/api/v1/sensors/Garage/summary",
        "/api/v1/garage/status",
        "/api/v1/garage/charts",
        "/api/v1/sump-pump/charts",
        "/api/v1/sump-pump/cycles",
        "/api/v1/hvac/cycles",
    ]
    for path in endpoints:
        response = api.get(path)
        assert response.status_code == 200, path


@pytest.mark.integration
def test_logs_endpoint(api):
    response = api.get("/api/v1/logs/collect")
    assert response.status_code == 200
    assert len(response.text) > 0
