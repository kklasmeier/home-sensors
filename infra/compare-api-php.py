#!/usr/bin/env python3
"""Compare FastAPI responses to legacy PHP on PiSensors."""
import json
import sys
import urllib.request


def get(url: str):
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read().decode())


def compare(name: str, php_url: str, api_url: str) -> bool:
    php, api = get(php_url), get(api_url)
    ok = php == api
    print(f"{name}: {'OK' if ok else 'DIFF'}")
    return ok


def main() -> int:
    base_php = "http://127.0.0.1"
    base_api = "http://127.0.0.1:8090/api/v1"
    all_ok = True

    all_ok &= compare(
        "sensor status",
        f"{base_php}/sensorStatus.php",
        f"{base_api}/sensors/status",
    )
    all_ok &= compare(
        "current readings",
        f"{base_php}/currentReadings.php",
        f"{base_api}/sensors/current",
    )
    all_ok &= compare(
        "garage summary",
        f"{base_php}/data_access.php?location=Garage",
        f"{base_api}/sensors/Garage/summary",
    )
    all_ok &= compare(
        "sump cycles",
        f"{base_php}/sumpPumpCycleData.php",
        f"{base_api}/sump-pump/cycles",
    )
    all_ok &= compare(
        "hvac cycles",
        f"{base_php}/HVACCycleData.php",
        f"{base_api}/hvac/cycles",
    )
    all_ok &= compare(
        "garage charts",
        f"{base_php}/garageDoorChartData.php",
        f"{base_api}/garage/charts",
    )
    all_ok &= compare(
        "sump charts",
        f"{base_php}/sumpPumpChartData.php",
        f"{base_api}/sump-pump/charts",
    )

    php_chart = get(f"{base_php}/chartData.php")
    api_chart = get(f"{base_api}/sensors/Garage/charts")
    php_garage = [r for r in php_chart if r.get("location") == "Garage"]
    ok = php_garage == api_chart
    print(f"garage sensor charts: {'OK' if ok else 'DIFF'}")
    all_ok &= ok

    for path in ("/docs", "/redoc"):
        status = urllib.request.urlopen(f"http://127.0.0.1:8090{path}").status
        print(f"{path}: {status}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
