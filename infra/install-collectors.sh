#!/bin/bash
# Install collector systemd units on PiSensors. Run on the Pi (or via ssh).
set -euo pipefail

REPO="/home/pi/home-sensors"
UNIT_DIR="/etc/systemd/system"

if [[ ! -f "$REPO/.env" ]]; then
  echo "Missing $REPO/.env — copy from .env.example and set DB_PASSWORD first." >&2
  exit 1
fi

for unit in "$REPO"/infra/systemd/home-sensors-collector-*.service; do
  sudo cp "$unit" "$UNIT_DIR/"
done

sudo systemctl daemon-reload

for unit in "$UNIT_DIR"/home-sensors-collector-*.service; do
  sudo systemctl enable "$(basename "$unit")"
done

echo "Installed. Start with: sudo systemctl start home-sensors-collector-{garage,attic,inside,outside,hvac,garagedoor,sump-pump}"
