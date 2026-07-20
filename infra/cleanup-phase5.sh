#!/bin/bash
# Phase 5 cleanup on PiSensors (requires sudo for archived web logs).
set -euo pipefail

if [[ -d /home/pi/HomeData/PythonScripts ]]; then
	rm -rf /home/pi/HomeData/PythonScripts
	echo "Removed /home/pi/HomeData/PythonScripts"
else
	echo "PythonScripts already removed"
fi

if [[ -d /var/www/html.archived ]]; then
	sudo rm -f /var/www/html.archived/query_log.txt /var/www/html.archived/php_errors.log
	echo "Removed archived PHP log files"
fi

echo "Done. Run: ./scripts/verify.sh --smoke"
