# Context for Cursor — home-sensors

Read this file **before** starting work. `build.md` has the phased plan and checklists; this file has the background, constraints, and answers to questions a new session would otherwise have to rediscover.

---

## What this project is

A **full modernization** of the Home Sensor Dashboard — a homelab app built in **2023** as a first AI-assisted project. It is still running in production today on **PiSensors** (`192.168.1.26`).

| Layer | Current (legacy) | Target (new) |
|-------|------------------|--------------|
| Ingest | Python scripts in `/home/pi/HomeData/PythonScripts/` | `collectors/` + systemd |
| Storage | MariaDB `homedata` | **Same database, same schema, same data** |
| API | ~12 PHP files in `/var/www/html/` | FastAPI in `api/` |
| UI | jQuery + Google Charts + `index.php` | SvelteKit in `web/` |
| Proxy | nginx port 80 | nginx port 80 (updated config only) |

**Goal:** Replace API and UI completely. Keep the data layer intact. No data loss. Other apps on the same Pi stay untouched.

---

## Cursor workspace

| Use this | Do NOT use this |
|----------|-----------------|
| `/home/pi/Programming/home-sensors` | `/home/pi/General Work/pisensors-rebuild-backup-20260613` |

- **Active project root:** `/home/pi/Programming/home-sensors` (NFS mount to PiSensors)
- **Deploy path on Pi:** `/home/pi/home-sensors` (same files via NFS)
- **Legacy backup (reference only):** `/home/pi/General Work/pisensors-rebuild-backup-20260613/` — old PHP, collectors, nginx configs from June 2026 rebuild backup. Consult when porting behavior; do not build there.

---

## Production URLs

| URL | Purpose |
|-----|---------|
| http://192.168.1.26/ | Current legacy dashboard (until cutover) |
| http://192.168.1.26:8090/ | New API during build (test port) |
| http://192.168.1.26:8090/docs | Swagger API docs (auto-generated) |
| http://192.168.1.26:8090/redoc | ReDoc API docs |

---

## Current UI — feature parity checklist

The new SvelteKit UI must match these capabilities (with a modern look):

### Sensor status grid
Seven tiles, color-coded by data freshness (green / yellow / red based on seconds since last reading):
- Attic
- Garage
- Inside
- Outside
- Garagedoor
- Sump Pump
- HVAC

Each tile shows location name + time since last reading (e.g. `Attic: 02:15`).

### Garage door panel
- **Main Garage Door** and **3rd Car Door**
- Open/closed image (`GarageOpen.jpg` / `GarageClosed.jpg` in legacy)
- Duration in current state (e.g. "0 hours, 57 minutes")

### Charts (Google Charts in legacy → modern chart lib in new UI)
- Temperature
- Heat index
- Humidity
- Pressure
- Sump pump activity
- Sump pump cycles
- HVAC cycles
- Garage door history

### Summary tables
Per-location high/low values for: temperature, heat index, humidity, pressure — across intervals: hour, day, week, month, year. (Legacy: `data_access.php` + `tables.html` pattern.)

### Log viewer
- "Show Logs" button opens a modal/popup with `collect_data.log` content
- Legacy uses Prism.js for syntax highlighting

### Auto-refresh
- Legacy refreshes every **300 seconds** (5 min) via `<meta http-equiv="refresh">`
- New UI should use a sensible polling interval or manual refresh (improvement OK)

---

## IoT sensor layer

Collectors poll Raspberry Pi Pico / ESP nodes over HTTP:

```
GET http://<sensor-ip>/data.json
```

Poll interval: **60 seconds** per collector.

### Sensor nodes (collector args)

| Script | IP | Location / type |
|--------|-----|-----------------|
| `collect_data.py` | 192.168.1.23 | Garage |
| `collect_data.py` | 192.168.1.30 | Attic |
| `collect_data.py` | 192.168.1.31 | Inside |
| `collect_data.py` | 192.168.1.36 | Outside |
| `collect_data.py` | 192.168.1.25 | HVAC |
| `collect_data_garagedoor.py` | 192.168.1.35 | Garage door |
| `get_sensor_data_sump_pump.py` | 192.168.1.37 | Sump pump |

### Expected JSON fields (temp/humidity sensors)
```json
{
  "Temperature_F": 72.5,
  "Heat Index_F": 74.0,
  "Humidity_%": 45.0,
  "Pressure_inHg": 30.12
}
```

Collectors validate these fields before insert. See legacy `collect_data.py` in `/home/pi/HomeData/PythonScripts/`.

---

## Database

| Setting | Value |
|---------|-------|
| Host | `localhost` (on PiSensors) |
| Database | `homedata` |
| User | `hu` |
| Password | **Leave unchanged** — load from `.env`, never commit |

Legacy connection reference: `/var/www/html/db_connection.php`

### Tables (do not alter schema in v1)

| Table | Purpose |
|-------|---------|
| `sensor_readings` | Raw readings: temp, heat index, humidity, pressure per location |
| `sensor_readings_summary` | Daily min/max rollups per location |
| `sensor_readings_garage` | Garage door open/closed events |
| `sensor_readings_sump_pump` | Sump pump on/off events |
| `sensor_readings_backup` | Archived duplicate readings (maintenance) |

### Key columns (`sensor_readings`)
- `reading_dttm`, `location`, `temperature_f`, `heat_index_f`, `humidity_pct`, `pressure_inHg`

---

## Legacy PHP API files

### In scope — must be replicated in FastAPI

| PHP file | New endpoint |
|----------|--------------|
| `sensorStatus.php` | `GET /api/v1/sensors/status` |
| `currentReadings.php` | `GET /api/v1/sensors/current` |
| `chartData.php` | `GET /api/v1/sensors/{location}/charts` |
| `data_access.php` | `GET /api/v1/sensors/{location}/summary` |
| `garageDoorStatus.php` | `GET /api/v1/garage/status` |
| `garageDoorChartData.php` | `GET /api/v1/garage/charts` |
| `sumpPumpChartData.php` | `GET /api/v1/sump-pump/charts` |
| `sumpPumpCycleData.php` | `GET /api/v1/sump-pump/cycles` |
| `HVACCycleData.php` | `GET /api/v1/hvac/cycles` |
| (log viewer) | `GET /api/v1/logs/collect` |

### Out of scope — do not port unless user confirms

| PHP file | Notes |
|----------|-------|
| `AN_GarageDoorStatus.php` | Likely unused analytics variant |
| `AN_SensorAlarmsData.php` | Likely unused analytics variant |
| `phpstats.php` | PHP stats/debug |
| `index.html` | Superseded by `index.php` |

When implementing, **compare JSON output** of new endpoints against live PHP responses on PiSensors.

---

## PiSensors runtime environment

| Component | Version / path |
|-----------|----------------|
| OS | Raspberry Pi OS (Debian Trixie), hostname `PiSensors` |
| MariaDB | 11.8, database `homedata` |
| nginx | `/etc/nginx/sites-enabled/` — **only modify `default` (port 80)** |
| PHP | 8.4-fpm (legacy only, until cutover) |
| Python | 3.x, `mysql.connector` / `requests` in collectors |
| Collector logs | `/home/pi/HomeData/Logs/collect_data.log` |
| Legacy web root | `/var/www/html/` |

### Other nginx sites — DO NOT MODIFY

| Port | App | Root / backend |
|------|-----|----------------|
| 8080 | Network traffic monitor | `/var/www/networktraffic` |
| 8000 | VPN gateway + camera API proxy | proxy → `:8001`, `:8002` |
| 8888 | Security camera UI | `/home/pi/Security-Camera-Central/www` |

---

## Auth and API consumers

- **No authentication in v1** — LAN-trust only, consistent with network traffic monitor and security camera API on the same Pi.
- **Future use:** Other homelab apps will call `/api/v1/...` programmatically. Design clean REST + OpenAPI docs; auth can be added later if needed.
- **Do not introduce** API keys, Basic auth, or Bearer tokens unless the user explicitly requests it.

---

## GitHub

| Item | Value |
|------|-------|
| Repo | https://github.com/kklasmeier/home-sensors |
| Visibility | Public (read) |
| Clone | `git@github.com:kklasmeier/home-sensors.git` |
| Auth on pi5Desktop | SSH — already configured, no API key needed |

### Branch protection (Ruleset on `main`)
- Require pull request before merging
- Required approvals: **0** (solo developer)
- Block force pushes
- Restrict deletions
- **Workflow:** `dev` branch → PR → merge to `main`

### Never commit
- `.env` (real credentials)
- `*.log`, `query_log.txt`, `php_errors.log`
- `node_modules/`, `venv/`, `__pycache__/`
- `bak*/` folders
- Secrets from legacy backup

---

## NFS dev environment

| Machine | Role | IP |
|---------|------|-----|
| pi5Desktop | Dev (Cursor) | 192.168.1.42 |
| PiSensors | Deploy / run | 192.168.1.26 |

- NFS export: `192.168.1.26:/home/pi/home-sensors` → `/home/pi/Programming/home-sensors`
- Boot-safe fstab: `nofail`, `x-systemd.automount`, `soft`, `_netdev`
- Edits on pi5Desktop are immediately on PiSensors filesystem

```bash
# Verify mount
mountpoint /home/pi/Programming/home-sensors
```

---

## Constraints (hard rules)

1. **Do not change** MariaDB schema or delete historical data.
2. **Do not rotate** the DB password (move to `.env` only).
3. **Do not modify** nginx configs for ports 8080, 8000, 8888.
4. **Do not touch** network traffic, VPN gateway, or security camera apps.
5. **Do not port** AI features.
6. **Run new collectors in parallel** with cron before disabling cron.
7. **Delete `bak*` folders** only at end of project (Phase 5), not needed in Git.
8. **Test API on :8090** before cutover to nginx port 80.

---

## Legacy collector cron (PiSensors — active until Phase 1 complete)

Full paths on PiSensors:

```
@reboot sleep 50; python3 /home/pi/HomeData/PythonScripts/collect_data_garagedoor.py 192.168.1.35 >> /home/pi/HomeData/Logs/collect_data.log 2>&1
@reboot sleep 55; python3 /home/pi/HomeData/PythonScripts/get_sensor_data_sump_pump.py 192.168.1.37 >> /home/pi/HomeData/Logs/collect_data.log 2>&1
@reboot sleep 60; python3 /home/pi/HomeData/PythonScripts/collect_data.py 192.168.1.23 Garage >> /home/pi/HomeData/Logs/collect_data.log 2>&1
@reboot sleep 65; python3 /home/pi/HomeData/PythonScripts/collect_data.py 192.168.1.30 Attic >> /home/pi/HomeData/Logs/collect_data.log 2>&1
@reboot sleep 70; python3 /home/pi/HomeData/PythonScripts/collect_data.py 192.168.1.31 Inside >> /home/pi/HomeData/Logs/collect_data.log 2>&1
@reboot sleep 75; python3 /home/pi/HomeData/PythonScripts/collect_data.py 192.168.1.36 Outside >> /home/pi/HomeData/Logs/collect_data.log 2>&1
@reboot sleep 75; python3 /home/pi/HomeData/PythonScripts/collect_data.py 192.168.1.25 HVAC >> /home/pi/HomeData/Logs/collect_data.log 2>&1
```

Weekly log rotation (keep running):
```
0 4 * * 6 /bin/bash /home/pi/HomeData/Logs/renameLogs.sh >> /home/pi/HomeData/Logs/renameLogs.log 2>&1
```

---

## Suggested first prompt (new Cursor session)

```
Continue the home-sensors rebuild.
Read docs/CONTEXT.md and build.md first.
Workspace: /home/pi/Programming/home-sensors
Start Phase 0: init git, connect to GitHub, scaffold folders, .gitignore, .env.example, README.
Do not modify legacy systems on PiSensors during Phase 0.
```

---

## Where to look when stuck

| Need | Location |
|------|----------|
| Build phases & checklists | `build.md` |
| Legacy PHP behavior | `/var/www/html/` on PiSensors (live) |
| Legacy collector code | `/home/pi/HomeData/PythonScripts/` on PiSensors |
| Backup snapshot | `/home/pi/General Work/pisensors-rebuild-backup-20260613/` |
| Gateway project patterns (FastAPI, systemd, .env) | `/home/pi/klasmeier-pi-gateway-ui/` on pi5Desktop |
| Security camera API patterns | `/home/pi/Security-Camera-Central/` (NFS mount) |
