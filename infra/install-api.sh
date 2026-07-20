#!/bin/bash
# Install Home Sensors API venv + systemd unit on PiSensors.
set -euo pipefail

REPO="/home/pi/home-sensors"
VENV="$REPO/api/venv"

if [[ ! -f "$REPO/.env" ]]; then
  echo "Missing $REPO/.env — copy from .env.example and set DB_PASSWORD first." >&2
  exit 1
fi

python3 -m venv "$VENV"
"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install -r "$REPO/api/requirements.txt"

sudo cp "$REPO/infra/systemd/home-sensors-api.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable home-sensors-api.service

echo "Installed. Start with: sudo systemctl start home-sensors-api"
echo "API docs: http://192.168.1.26:8090/docs"
