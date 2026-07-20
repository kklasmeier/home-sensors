#!/bin/bash
# Remove legacy @reboot collector cron entries (run on PiSensors after systemd collectors verified).
set -euo pipefail

TMP="$(mktemp)"
crontab -l | grep -v 'HomeData/PythonScripts/collect_data' | grep -v 'get_sensor_data_sump_pump' > "$TMP"
crontab "$TMP"
rm "$TMP"
echo "Removed legacy collector @reboot entries. Remaining crontab:"
crontab -l
