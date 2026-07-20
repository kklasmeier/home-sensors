# Testing — home-sensors

How automated verification works for this project. Run checks on **PiSensors** after deploys; run unit tests on **pi5Desktop** anytime.

## Layout

```
home-sensors/
├── tests/                      # pytest suite
│   ├── conftest.py             # shared fixtures (mocked DB, TestClient)
│   ├── test_serialize.py       # pure unit tests
│   ├── test_sensors.py         # status color logic
│   ├── test_api_contract.py    # API response shapes (mocked DB)
│   └── test_integration.py     # live API tests (skipped by default)
├── scripts/
│   └── verify.sh               # one-command post-deploy verification
├── infra/
│   └── compare-api-php.py      # FastAPI vs legacy PHP JSON parity
├── pytest.ini                  # pytest config and markers
└── requirements-dev.txt        # pytest, httpx (+ api deps)
```

Test **infra** is intentionally split:

| Location | Role |
|----------|------|
| `tests/` | Python unit + integration tests |
| `scripts/verify.sh` | Orchestrator: systemd, HTTP smoke, parity, pytest |
| `infra/compare-api-php.py` | PHP parity checker (used by `verify.sh`) |

## Quick start

### On PiSensors (full verification)

```bash
cd /home/pi/home-sensors
./scripts/verify.sh
```

This checks:

1. All 7 collector systemd units are `active`
2. `home-sensors-api` is `active`
3. Every v1 HTTP endpoint returns 200
4. FastAPI JSON matches legacy PHP (until Phase 4 cutover)
5. Unit tests pass (`pytest` via API venv)

### On pi5Desktop (unit tests only)

```bash
cd /home/pi/Programming/home-sensors
python3 -m venv api/venv
api/venv/bin/pip install -r requirements-dev.txt
pytest -q
```

No Pi services or database required — DB access is mocked.

## verify.sh options

```bash
./scripts/verify.sh              # full check (default)
./scripts/verify.sh --smoke      # skip PHP parity (use after Phase 4 cutover)
./scripts/verify.sh --no-pytest  # skip unit tests (faster smoke only)
RUN_INTEGRATION=1 ./scripts/verify.sh  # also run live integration tests
```

Environment overrides:

| Variable | Default | Purpose |
|----------|---------|---------|
| `API_BASE` | `http://127.0.0.1:8090` | FastAPI base URL |
| `PHP_BASE` | `http://127.0.0.1` | Legacy PHP base URL |
| `RUN_INTEGRATION` | `0` | Set to `1` to enable `@integration` tests |

## Test layers

### 1. Unit tests (`pytest`, default)

- **No network, no DB** — `get_connection` is mocked in `conftest.py`
- Covers serialization helpers, status color thresholds, response shapes, OpenAPI paths
- Run anywhere: `pytest -q`

### 2. Smoke tests (`verify.sh`)

- Confirms systemd services and HTTP 200 on all v1 routes
- Runs on PiSensors only (services must be installed)

### 3. PHP parity (`infra/compare-api-php.py`)

- Side-by-side JSON comparison with legacy PHP on port 80
- **Temporary** — drop after Phase 4 when PHP is retired; use `./scripts/verify.sh --smoke` instead
- Live endpoints (`sensor status`) allow ±5s drift on `diff_seconds`; `current readings` checks structure when values drift between requests

### 4. Integration tests (`tests/test_integration.py`)

- Hit the real API on PiSensors
- **Skipped by default** — enable with `RUN_INTEGRATION=1 pytest -m integration`
- `verify.sh` runs these when `RUN_INTEGRATION=1` is set

## When to run what

| Event | Command |
|-------|---------|
| After Phase deploy on Pi | `./scripts/verify.sh` |
| After API code change (local) | `pytest -q` |
| Before merging `dev` → `main` | `./scripts/verify.sh` on Pi |
| After Phase 4 cutover | `./scripts/verify.sh --smoke` |
| Phase 3+ frontend (future) | extend `verify.sh` / add Playwright |

## Adding tests

- **New API endpoint** → add mocked contract test in `tests/test_api_contract.py`, add path to `verify.sh` `ENDPOINTS` array, add PHP compare row if parity still needed
- **New pure logic** → add `tests/test_<module>.py`
- **Live-only behavior** → add `@pytest.mark.integration` test in `test_integration.py`

## CI note

Full integration tests require PiSensors (MariaDB + systemd). GitHub Actions can run `pytest -q` (unit only) on push; Pi-hosted `verify.sh` remains the source of truth for deploy verification.
