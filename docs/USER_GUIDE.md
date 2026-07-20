# Home Sensor Dashboard — User Guide

The **Home Sensor Dashboard** shows live and historical readings from sensors around the house: temperature, humidity, pressure, garage doors, sump pump, and HVAC activity. Data is collected automatically every minute and stored on the homelab server **PiSensors**.

---

## Accessing the dashboard

| What | URL |
|------|-----|
| **Dashboard (main page)** | http://192.168.1.26/ |
| **API documentation** (technical) | http://192.168.1.26/docs |

**Requirements**

- You must be on the home network (LAN). The dashboard is not exposed to the internet.
- No login or password is required.
- Use any modern browser (Chrome, Firefox, Safari, Edge). The layout works on phones and tablets.

Open the dashboard URL in your browser and leave the tab open; it refreshes itself.

---

## How the site is organized

The dashboard uses **multiple pages** so you are not scrolling through every chart at once.

| Page | URL | What's there |
|------|-----|----------------|
| **Home** | http://192.168.1.26/ | Status tiles, garage doors, current readings, links to detail pages |
| **Location** | `/locations/Attic`, `/locations/Garage`, etc. | One room: current values, 24h charts, high/low summary |
| **Garage doors** | `/systems/garage-doors` | Door images, status, 24h history chart |
| **Sump pump** | `/systems/sump-pump` | Water level chart and daily cycle counts |
| **HVAC cycles** | `/systems/hvac` | Daily HVAC cycle chart (env readings on `/locations/HVAC`) |
| **Collector logs** | `/logs` | Last 2000 lines from `collect_data.log` |

From **Home**, use the **Locations** and **Systems** cards to open a detail page. Use the **header link**, **← Back to overview**, **Logs** in the header, or **Home** in the breadcrumbs to navigate.

```text
HOME (/)
├── Status tiles + garage doors + current readings table
├── Location cards → /locations/Attic, /locations/Inside, …
└── System cards   → /systems/garage-doors, /systems/sump-pump, /systems/hvac

/locations/Inside
├── Current readings for Inside
├── Temperature, heat index, humidity, pressure charts (24h)
└── High / low summary table for Inside only

/systems/sump-pump
├── Water level chart (24h)
└── Cycles per day (bar chart)
```

Every page has **Show Logs**, **Refresh now**, and the same **60-second** auto-refresh.

---

## Home page

The home page is your **whole-house snapshot**:

1. **Toolbar** — logs, last update time, manual refresh
2. **Sensor status tiles** — quick health check for each data source
3. **Garage doors** — open/closed state and how long each door has been in that state
4. **Current readings** — latest temperature, heat index, humidity, and pressure per room
5. **Location cards** — open a room for charts and summaries
6. **System cards** — open garage-door history, sump pump, or HVAC cycles

---

## Sensor status tiles

Seven tiles show how recently each sensor last reported data:

| Tile | Monitors |
|------|----------|
| **Attic** | Attic temperature / humidity sensor |
| **Garage** | Garage environment sensor |
| **Inside** | Indoor temperature / humidity sensor |
| **Outside** | Outdoor temperature / humidity sensor |
| **Garagedoor** | Garage door open/close sensors |
| **Sump Pump** | Basement sump pump water level |
| **HVAC** | HVAC-related readings |

Each tile shows the location name and **time since the last reading** (for example `02:15` means 2 minutes 15 seconds ago, or `1:05:30` when over an hour).

### Tile colors

| Color | Meaning | Typical cause |
|-------|---------|----------------|
| **Green** | Healthy — last reading within **3 minutes** | Normal operation |
| **Yellow** | Stale — last reading **3–10 minutes** ago | Brief network blip or sensor reboot |
| **Red** | Offline — no reading for **more than 10 minutes** | Sensor powered off, Wi‑Fi issue, or hardware fault |
| **Gray** | No data | Sensor has never reported or location not configured |

A red tile does not always mean the room is dangerously hot or cold; it usually means **the dashboard is not receiving new data** from that sensor. Other sections may still show the last stored values until they age out.

---

## Garage doors

Two panels show the **Main Garage Door** and **3rd Car Door**:

| Display | Meaning |
|---------|---------|
| Open garage image | Door is **open** (sensor reports `UP`) |
| Closed garage image | Door is **closed** (sensor reports `DOWN`) |
| Status line | `UP` or `DOWN` |
| Duration | How long the door has been in the current state (e.g. `0 hours, 57 minutes`) |

The **Garage Door History** chart is on **Systems → Garage Doors** (`/systems/garage-doors`).

---

## Current readings

A table lists the **most recent** environment readings for each location:

| Column | Unit / notes |
|--------|----------------|
| **Temperature** | Degrees Fahrenheit (°F) |
| **Heat Index** | Feels-like temperature (°F) |
| **Humidity** | Percent relative humidity (%) |
| **Pressure** | Barometric pressure (inHg) |

Locations: Attic, Garage, Inside, Outside, HVAC.

A dash (**—**) means no reading is available for that location (often because the sensor is offline).

---

## Location pages

Open a location from the home page (e.g. **Inside**) to see:

- **Current** — temperature, heat index, humidity, pressure, and status for that room only
- **Last 24 hours** — four line charts (temperature, heat index, humidity, pressure)
- **High / low summary** — one table for that location across HOUR, DAY, WEEK, MONTH, YEAR

Locations: **Attic**, **Garage**, **Inside**, **Outside**, **HVAC**.

---

## System pages

| Page | Charts and data |
|------|-----------------|
| **Garage Doors** | Door panels plus 24h open/closed history for Main and 3rd-car doors |
| **Sump Pump** | Water level (24h line chart) and cycles per day (bar chart) |
| **HVAC Cycles** | HVAC cycles per day (bar chart). For temp/humidity at the HVAC sensor, use **Locations → HVAC**. |

---

## Charts (all pages)

Line charts on location and system pages use the **last 24 hours** of data unless noted as daily cycle counts.

| Where | Charts |
|-------|--------|
| Each **location** page | Temperature, heat index, humidity, pressure (that location only) |
| **Garage Doors** | Door state history (both doors) |
| **Sump Pump** | Water level; daily cycle bar chart |
| **HVAC Cycles** | Daily cycle bar chart |

Hover over a chart to see exact values and timestamps. On a phone, scroll horizontally if a table or chart is wider than the screen.

---

## Summary tables

On each **location** page, one table lists **high / low** values for:

- Temperature  
- Heat Index  
- Humidity  
- Pressure  

Columns are time ranges: **HOUR**, **DAY**, **WEEK**, **MONTH**, **YEAR**.

| Color in cell | Meaning |
|---------------|---------|
| **Red (first number)** | High for that period |
| **Blue (second number)** | Low for that period |

Example: `72.5 / 68.1` under **DAY** for Temperature means the daily high was 72.5 °F and the low was 68.1 °F.

**N/A** means there was not enough data for that interval.

---

## Toolbar (every page)

The **site header** at the top always shows **Home Sensor Dashboard** (links home) and **Logs** (links to `/logs`). On detail pages, **← Back to overview** appears on the right.

**Breadcrumbs** under the header show where you are, e.g. `Home / Inside` or `Home / Collector Logs`. Click **Home** in the trail to go back.

| Control | What it does |
|---------|----------------|
| **Logs** (header) | Opens the collector log page — last 2000 lines, auto-refreshes every 60s |
| **Refresh now** | Reloads page data immediately instead of waiting for the next automatic refresh |
| **Updated … · auto-refresh every 60s** | Shows when data was last loaded. Pages poll every **60 seconds** while the tab is open. |

If the server is unreachable, a red error banner appears at the top. Try **Refresh now** or check that you are on the home network.

---

## What is being measured?

Small **Raspberry Pi Pico / ESP** devices on the home network expose readings over HTTP. A collector service on PiSensors polls them about **once per minute** and saves results to the database. The dashboard reads from that database; it does not talk to the sensors directly.

| Location | Role |
|----------|------|
| Garage | Temperature, humidity, pressure in the garage |
| Attic | Attic conditions |
| Inside | Indoor conditions |
| Outside | Outdoor conditions |
| HVAC | HVAC-related environmental readings |
| Garage doors | Open/closed state (two doors) |
| Sump pump | Basement water level and pump activity |

Historical data is kept long term, so charts and summary tables can show trends across days, weeks, and years.

---

## Troubleshooting (for users)

| Symptom | What to try |
|---------|-------------|
| Page will not load | Confirm you are on the home Wi‑Fi or LAN. Try http://192.168.1.26/ in a private/incognito window. |
| One tile stays **red** | That sensor or its network path may be down. Other tiles can still be green. |
| Values look old | Click **Refresh now**. Check the tile color for that location. |
| Garage image wrong | Door sensor may be offline; check the **Garagedoor** tile. |
| Need more detail | Open **Logs** in the header and look for errors mentioning the location name. Share a screenshot with whoever maintains PiSensors. |

This dashboard is for **monitoring only**. It does not control garage doors, HVAC, or the sump pump.

---

## Other apps on the same server

PiSensors hosts other homelab tools on different ports. They are separate from the sensor dashboard:

| Port | App |
|------|-----|
| **80** | Home Sensor Dashboard (this app) |
| 8080 | Network traffic monitor |
| 8000 | VPN gateway and camera API |
| 8888 | Security camera UI |

---

## For administrators

Installation, deployment, API details, and development workflow are documented in the repository:

| Document | Audience |
|----------|----------|
| [README.md](../README.md) | Quick orientation and repo layout |
| [build.md](../build.md) | Phased build plan and project history |
| [docs/CONTEXT.md](CONTEXT.md) | Architecture and constraints for developers |
| [docs/TESTING.md](TESTING.md) | Automated tests and smoke checks |
| http://192.168.1.26/docs | Interactive API reference (OpenAPI) |
