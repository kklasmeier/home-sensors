#!/bin/bash
# Phase 4 cutover: nginx port 80 → new UI + API proxy; archive legacy PHP.
set -euo pipefail

REPO="/home/pi/home-sensors"
DIST="$REPO/web/dist"

build_frontend() {
	if command -v npm >/dev/null 2>&1; then
		echo "=== Production frontend build (same-origin /api) ==="
		cd "$REPO/web"
		VITE_API_BASE= npm run build
	elif [[ -f "$DIST/index.html" ]]; then
		echo "=== Frontend build skipped (no npm on Pi; using existing web/dist from NFS) ==="
	else
		echo "ERROR: npm not found and $DIST/index.html is missing." >&2
		echo "Build on pi5Desktop: cd ~/Programming/home-sensors/web && VITE_API_BASE= npm run build" >&2
		exit 1
	fi
}

build_frontend

echo ""
echo "=== Install nginx site (port 80) ==="
sudo cp "$REPO/infra/nginx/default" /etc/nginx/sites-available/default
sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

echo ""
echo "=== Archive legacy PHP site ==="
if [[ -d /var/www/html && ! -e /var/www/html.archived ]]; then
	sudo mv /var/www/html /var/www/html.archived
	echo "Archived to /var/www/html.archived"
elif [[ -d /var/www/html.archived ]]; then
	echo "Already archived (/var/www/html.archived exists)"
else
	echo "No /var/www/html to archive"
fi

if [[ -d /var/www/html.archived ]]; then
	echo "Removing bak* folders from archive..."
	sudo find /var/www/html.archived -depth -type d -name 'bak*' -exec rm -rf {} + 2>/dev/null || true
fi

echo ""
echo "=== Reload nginx ==="
sudo nginx -t
sudo systemctl reload nginx

echo ""
echo "Cutover complete."
echo "  Dashboard: http://192.168.1.26/"
echo "  API docs:  http://192.168.1.26/docs  (also :8090/docs)"
echo ""
echo "Run: ./scripts/verify.sh --smoke"
