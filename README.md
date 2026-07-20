# home-sensors

Modern replacement for the Home Sensor Dashboard on **PiSensors** (`192.168.1.26`). IoT collectors write to MariaDB; a FastAPI backend and SvelteKit frontend replace the legacy PHP + jQuery stack.

| Layer | Stack |
|-------|-------|
| Collectors | Python → MariaDB `homedata` |
| API | FastAPI (`/api/v1/...`) |
| UI | SvelteKit |
| Proxy | nginx (port 80) |

**Production:** http://192.168.1.26/  
**API docs:** http://192.168.1.26/docs (direct: http://192.168.1.26:8090/docs)

### Documentation

| Guide | Audience |
|-------|----------|
| **[docs/USER_GUIDE.md](docs/USER_GUIDE.md)** | End users — how to read the dashboard |
| [build.md](build.md) | Build phases and checklists |
| [docs/CONTEXT.md](docs/CONTEXT.md) | Architecture and handoff for developers |
| [docs/TESTING.md](docs/TESTING.md) | Tests and smoke verification |

### Cutover (Phase 4)

On PiSensors:

```bash
bash /home/pi/home-sensors/infra/cutover.sh
./scripts/verify.sh --smoke
```

## Repo layout

```
home-sensors/
├── collectors/     # Python ingest + systemd units
├── api/            # FastAPI application
├── web/            # SvelteKit frontend
├── infra/          # nginx and systemd configs
│   ├── nginx/
│   └── systemd/
├── docs/           # Architecture and handoff notes
├── build.md        # Phased build plan and progress
└── .env.example    # Copy to .env on PiSensors (not committed)
```

## Dev workflow

Code is edited on **pi5Desktop** via NFS mount; files live on PiSensors at `/home/pi/home-sensors`.

| Machine | Path |
|---------|------|
| pi5Desktop (Cursor) | `/home/pi/Programming/home-sensors` |
| PiSensors (runtime) | `/home/pi/home-sensors` |

```bash
# Verify NFS mount on pi5Desktop
mountpoint /home/pi/Programming/home-sensors
```

1. Edit in Cursor on pi5Desktop.
2. Restart services on PiSensors when needed (e.g. `sudo systemctl restart home-sensors-api`).
3. Frontend dev server on pi5Desktop; point API at `http://192.168.1.26:8090`.

## Configuration

```bash
cp .env.example .env
# Edit .env on PiSensors with real DB credentials (same password as legacy; do not rotate)
```

## Build progress

See **[build.md](build.md)** for phased plan, API contract, and checklists. New sessions should read **[docs/CONTEXT.md](docs/CONTEXT.md)** first.

## Git workflow

- Develop on `dev`, open PR to `main`.
- Do not commit `.env`, logs, `venv/`, `node_modules/`, or `bak*/` folders.

## Related homelab apps (same Pi, untouched)

| Port | App |
|------|-----|
| 8080 | Network traffic monitor |
| 8000 | VPN gateway + camera API proxy |
| 8888 | Security camera UI |
