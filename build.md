# home-sensors — Build Plan & Progress

Modernize the Home Sensor Dashboard on **PiSensors** (`192.168.1.26`).

> **New session?** Read [`docs/CONTEXT.md`](docs/CONTEXT.md) first for background, feature parity, legacy paths, constraints, and the suggested starter prompt. This file tracks phases and checklists.

| Item | Value |
|------|-------|
| **Repo** | https://github.com/kklasmeier/home-sensors |
| **Dev machine** | pi5Desktop (`192.168.1.42`) |
| **Deploy target** | PiSensors (`192.168.1.26`) |
| **Code path (Pi)** | `/home/pi/home-sensors` |
| **Dev mount (Desktop)** | `/home/pi/Programming/home-sensors` |
| **Production URL** | http://192.168.1.26/ |
| **API test URL** | http://192.168.1.26:8090/ |
| **API docs** | http://192.168.1.26:8090/docs |

---

## Decisions (locked)

| Topic | Decision |
|-------|----------|
| Scope | Sensor system only — network traffic, VPN gateway, security cameras **untouched** |
| Data layer | Keep MariaDB `homedata` schema and all historical data **unchanged** |
| Collectors | Move to `collectors/`, wrap in systemd; same DB writes |
| API | FastAPI replaces PHP; test on `:8090`, cutover to nginx `:80` |
| Frontend | SvelteKit — full UI facelift, feature parity with current dashboard |
| nginx | Keep as shared reverse proxy; only change port **80** block |
| Auth | **None** — LAN-open like other homelab apps (no API keys in v1) |
| API docs | FastAPI `/docs` + `/redoc` (auto-generated OpenAPI) |
| DB password | Leave as-is (move to `.env`, do not rotate) |
| Old `bak*` folders | Delete at end of project; not committed to Git |
| AI features | None |

---

## Architecture

```
IoT sensors (Pico/ESP @ LAN IPs)
        │  HTTP /data.json
        ▼
collectors/          ← Python, systemd, writes to MariaDB
        │
        ▼
MariaDB homedata     ← UNCHANGED schema + data
        │
        ▼
api/                 ← FastAPI on :8090 (test) → nginx /api/ (prod)
        │
        ▼
web/                 ← SvelteKit SPA, built to dist/, served by nginx
```

### nginx on PiSensors (unchanged except port 80)

| Port | App | Status |
|------|-----|--------|
| 80 | Home Sensor Dashboard | **Replacing** |
| 8080 | Network traffic monitor | Untouched |
| 8000 | VPN gateway + camera API proxy | Untouched |
| 8888 | Security camera UI | Untouched |

### API contract (v1 — mirrors current PHP)

| Endpoint | Replaces |
|----------|----------|
| `GET /api/v1/sensors/status` | `sensorStatus.php` |
| `GET /api/v1/sensors/current` | `currentReadings.php` |
| `GET /api/v1/sensors/{location}/charts` | `chartData.php` |
| `GET /api/v1/sensors/{location}/summary` | `data_access.php` |
| `GET /api/v1/garage/status` | `garageDoorStatus.php` |
| `GET /api/v1/garage/charts` | `garageDoorChartData.php` |
| `GET /api/v1/sump-pump/charts` | `sumpPumpChartData.php` |
| `GET /api/v1/sump-pump/cycles` | `sumpPumpCycleData.php` |
| `GET /api/v1/hvac/cycles` | `HVACCycleData.php` |
| `GET /api/v1/logs/collect` | `collect_data.log` viewer |

---

## Repo structure (target)

```
home-sensors/
├── collectors/          # Python ingest scripts + systemd units
├── api/                 # FastAPI application
├── web/                 # SvelteKit frontend
├── infra/
│   ├── nginx/         # Port 80 site config
│   └── systemd/       # Service unit files
├── docs/                # Architecture notes, API reference
├── .env.example
├── .gitignore
├── build.md             # This file
└── README.md
```

---

## Dev environment

### NFS mount (done)

- **Pi export:** `/home/pi/home-sensors` → `192.168.1.42`
- **Desktop mount:** `/home/pi/Programming/home-sensors`
- **Boot-safe options:** `nofail`, `x-systemd.automount`, `soft`, `_netdev`

```bash
# Verify mount
mountpoint /home/pi/Programming/home-sensors
```

### Workflow

1. Edit code in Cursor at `/home/pi/Programming/home-sensors`
2. Changes are immediately on PiSensors filesystem (NFS)
3. Restart services on Pi to pick up changes:
   ```bash
   ssh pi@192.168.1.26 'sudo systemctl restart home-sensors-api'
   ```
4. Frontend dev server runs on pi5Desktop, API pointed at `192.168.1.26:8090`
5. Production build: `npm run build` → nginx serves `web/dist/`

---

## GitHub

- **Repo:** https://github.com/kklasmeier/home-sensors (public read)
- **Auth:** SSH from pi5Desktop (`git@github.com:kklasmeier/home-sensors.git`) — already configured
- **No API key needed** for git push over SSH

### Locking down writes (recommended)

Public repo = anyone can **read** code. To prevent unauthorized **writes**:

1. **GitHub → Settings → Branches → Branch protection rules → `main`:**
   - [ ] Require a pull request before merging
   - [ ] Require approvals: 0 (solo dev) or 1 if you want a sanity check
   - [ ] Do not allow bypassing the above settings
   - [ ] Restrict who can push to matching branches → only `kklasmeier`
2. **Workflow:** develop on `dev` branch → PR to `main` → merge
3. **Never commit:** `.env`, logs, credentials, `node_modules/`, `venv/`, `__pycache__/`
4. **Optional later:** GitHub Rulesets for additional enforcement

---

## Progress tracker

### Phase 0 — Foundation

- [x] NFS export on PiSensors (`/etc/exports`)
- [x] NFS mount on pi5Desktop (`/etc/fstab`, mount verified)
- [x] Decisions documented (this file)
- [x] Git repo initialized in `/home/pi/home-sensors`
- [x] Connected to GitHub remote
- [ ] GitHub Ruleset on `main` (PR required, block force push, restrict deletions) — configure in GitHub UI (`gh` not on pi5Desktop)
- [x] Folder structure created (`collectors/`, `api/`, `web/`, `infra/`, `docs/`)
- [x] `.gitignore` and `.env.example`
- [x] `README.md`

### Phase 1 — Collectors

- [ ] Copy collectors from `/home/pi/HomeData/PythonScripts/` → `collectors/`
- [ ] Extract DB creds to `.env` (same password, not hardcoded)
- [ ] Create systemd unit per collector:
  - [ ] `collect_data.py` — Garage (`.23`)
  - [ ] `collect_data.py` — Attic (`.30`)
  - [ ] `collect_data.py` — Inside (`.31`)
  - [ ] `collect_data.py` — Outside (`.36`)
  - [ ] `collect_data.py` — HVAC (`.25`)
  - [ ] `collect_data_garagedoor.py` (`.35`)
  - [ ] `get_sensor_data_sump_pump.py` (`.37`)
- [ ] Enable systemd units (parallel to existing cron)
- [ ] Verify data still flowing to MariaDB
- [ ] Disable cron `@reboot` collector entries
- [ ] Confirm systemd-only collectors running

### Phase 2 — API (FastAPI)

- [ ] Scaffold FastAPI app in `api/`
- [ ] Shared DB connection module (reads `.env`)
- [ ] Implement all v1 endpoints (see API contract above)
- [ ] Side-by-side JSON comparison: new API vs old PHP
- [ ] systemd service `home-sensors-api` on port `:8090`
- [ ] `/docs` and `/redoc` verified
- [ ] All endpoints return matching data

### Phase 3 — Frontend (SvelteKit)

- [ ] Scaffold SvelteKit app in `web/`
- [ ] Sensor status grid (color-coded, last-seen)
- [ ] Garage door panel (open/closed, duration)
- [ ] Charts: temperature, heat index, humidity, pressure
- [ ] Charts: sump pump, HVAC cycles, garage door
- [ ] Per-location summary tables (high/low by interval)
- [ ] Log viewer (collect_data.log)
- [ ] Responsive / mobile-friendly layout
- [ ] Dark mode
- [ ] `npm run build` → `web/dist/`

### Phase 4 — Cutover

- [ ] nginx config: port 80 serves `web/dist/` + proxies `/api/` to FastAPI
- [ ] FastAPI moved from `:8090` to unix socket or `:8090` behind nginx
- [ ] Full smoke test on http://192.168.1.26/
- [ ] Old PHP site disabled (stop serving `/var/www/html`)
- [ ] Archive `/var/www/html` → `/var/www/html.archived`
- [ ] Delete `bak*` folders in archived directory
- [ ] Update README with production URLs

### Phase 5 — Cleanup

- [ ] Remove `/home/pi/HomeData/PythonScripts/` old copies (after collectors verified in repo)
- [ ] Remove `query_log.txt`, `php_errors.log` from old web root
- [ ] Final commit + tag `v1.0.0`
- [ ] Verify all sensor data still flowing 24h after cutover

---

## Legacy reference (do not modify during build)

| Path | Purpose |
|------|---------|
| `/var/www/html/` | Current PHP dashboard (port 80) |
| `/home/pi/HomeData/PythonScripts/` | Current collectors (cron @reboot) |
| `/home/pi/HomeData/Logs/` | Collector logs |
| MariaDB `homedata` | Database — **read/write but no schema changes** |

### Current collector cron (on PiSensors)

```
@reboot sleep 50; python3 .../collect_data_garagedoor.py 192.168.1.35
@reboot sleep 55; python3 .../get_sensor_data_sump_pump.py 192.168.1.37
@reboot sleep 60; python3 .../collect_data.py 192.168.1.23 Garage
@reboot sleep 65; python3 .../collect_data.py 192.168.1.30 Attic
@reboot sleep 70; python3 .../collect_data.py 192.168.1.31 Inside
@reboot sleep 75; python3 .../collect_data.py 192.168.1.36 Outside
@reboot sleep 75; python3 .../collect_data.py 192.168.1.25 HVAC
```

### MariaDB tables (unchanged)

- `sensor_readings`
- `sensor_readings_summary`
- `sensor_readings_garage`
- `sensor_readings_sump_pump`
- `sensor_readings_backup`

---

## Session log

| Date | Notes |
|------|-------|
| 2026-07-19 | Assessed legacy PHP dashboard + Python collectors on PiSensors |
| 2026-07-19 | Locked architecture decisions; NFS mount configured and verified |
| 2026-07-19 | Created `build.md`; ready for Phase 0 git scaffold |
| 2026-07-19 | Added `docs/CONTEXT.md` for new Cursor session handoff |
| 2026-07-19 | Phase 0: git init, scaffold, `.gitignore`, `.env.example`, `README`, push to GitHub |
