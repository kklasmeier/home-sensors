#!/bin/bash
# Post-deploy verification for home-sensors on PiSensors.
#
# Usage:
#   ./scripts/verify.sh              # full check (systemd + smoke + PHP parity + unit tests)
#   ./scripts/verify.sh --smoke      # skip PHP parity (e.g. after Phase 4 cutover)
#   ./scripts/verify.sh --no-pytest  # skip unit tests
#
# Environment:
#   API_BASE=http://127.0.0.1:8090
#   PHP_BASE=http://127.0.0.1
#   RUN_INTEGRATION=1                # also run live integration pytest markers
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
WEB_BASE="${WEB_BASE:-http://127.0.0.1}"
API_BASE="${API_BASE:-http://127.0.0.1:8090}"
PHP_BASE="${PHP_BASE:-http://127.0.0.1}"
RUN_PHP_PARITY=1
RUN_PYTEST=1
RUN_INTEGRATION_TESTS="${RUN_INTEGRATION:-0}"

for arg in "$@"; do
  case "$arg" in
    --smoke) RUN_PHP_PARITY=0 ;;
    --no-pytest) RUN_PYTEST=0 ;;
    -h|--help)
      sed -n '2,12p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown option: $arg" >&2
      exit 2
      ;;
  esac
done

COLLECTORS=(
  home-sensors-collector-garage
  home-sensors-collector-attic
  home-sensors-collector-inside
  home-sensors-collector-outside
  home-sensors-collector-hvac
  home-sensors-collector-garagedoor
  home-sensors-collector-sump-pump
)

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

echo "=== Collectors (systemd) ==="
for unit in "${COLLECTORS[@]}"; do
  state="$(systemctl is-active "$unit" 2>/dev/null || echo inactive)"
  echo "$unit: $state"
  [[ "$state" == "active" ]] || fail "$unit is not active"
done

echo ""
echo "=== API service (systemd) ==="
api_state="$(systemctl is-active home-sensors-api 2>/dev/null || echo inactive)"
echo "home-sensors-api: $api_state"
[[ "$api_state" == "active" ]] || fail "home-sensors-api is not active"

echo ""
echo "=== HTTP smoke ($API_BASE) ==="
curl -sf "$API_BASE/" >/dev/null || fail "API root unreachable"
curl -sf "$API_BASE/docs" >/dev/null || fail "/docs unreachable"
curl -sf "$API_BASE/redoc" >/dev/null || fail "/redoc unreachable"

ENDPOINTS=(
  /api/v1/sensors/status
  /api/v1/sensors/current
  /api/v1/sensors/Garage/charts
  /api/v1/sensors/Garage/summary
  /api/v1/garage/status
  /api/v1/garage/charts
  /api/v1/sump-pump/charts
  /api/v1/sump-pump/cycles
  /api/v1/hvac/cycles
)
for path in "${ENDPOINTS[@]}"; do
  code="$(curl -s -o /dev/null -w '%{http_code}' "$API_BASE$path")"
  echo "$path: $code"
  [[ "$code" == "200" ]] || fail "$path returned $code"
done

log_code="$(curl -s -o /dev/null -w '%{http_code}' "$API_BASE/api/v1/logs/collect")"
echo "/api/v1/logs/collect: $log_code"
[[ "$log_code" == "200" ]] || fail "logs endpoint returned $log_code"

echo ""
echo "=== Production smoke ($WEB_BASE via nginx) ==="
curl -sf "$WEB_BASE/" >/dev/null || fail "dashboard root unreachable"
prod_code="$(curl -s -o /dev/null -w '%{http_code}' "$WEB_BASE/api/v1/sensors/status")"
echo "/api/v1/sensors/status (proxied): $prod_code"
[[ "$prod_code" == "200" ]] || fail "proxied API returned $prod_code"
curl -sf "$WEB_BASE/docs" >/dev/null || fail "proxied /docs unreachable"

if [[ "$RUN_PHP_PARITY" == "1" ]]; then
  echo ""
  echo "=== PHP parity ==="
  python3 "$REPO/infra/compare-api-php.py" || fail "PHP parity check failed"
else
  echo ""
  echo "=== PHP parity skipped (--smoke) ==="
fi

if [[ "$RUN_PYTEST" == "1" ]]; then
  echo ""
  echo "=== Unit tests (pytest) ==="
  VENV="$REPO/api/venv"
  if [[ ! -x "$VENV/bin/python" ]]; then
    python3 -m venv "$VENV"
  fi
  "$VENV/bin/pip" install -q -r "$REPO/requirements-dev.txt"
  (cd "$REPO" && "$VENV/bin/pytest" -q)
  if [[ "$RUN_INTEGRATION_TESTS" == "1" ]]; then
    echo ""
    echo "=== Integration tests (live API) ==="
    (cd "$REPO" && RUN_INTEGRATION=1 "$VENV/bin/pytest" -q -m integration)
  fi
fi

echo ""
echo "All verification checks passed."
