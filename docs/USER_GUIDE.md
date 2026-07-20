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

## Page overview

The dashboard is a single scrolling page with these sections, top to bottom:

1. **Toolbar** — logs, last update time, manual refresh
2. **Sensor status tiles** — quick health check for each data source
3. **Garage doors** — open/closed state and how long each door has been in that state
4. **Current readings** — latest temperature, heat index, humidity, and pressure per room
5. **Charts** — trends over the last 24 hours (or daily cycle counts where noted)
6. **Summary tables** — high and low values by hour, day, week, month, and year

```text
┌─────────────────────────────────────────────────────────┐
│  Home Sensor Dashboard          [Show Logs] [Refresh]   │
├─────────────────────────────────────────────────────────┤
│  [Attic] [Garage] [Inside] [Outside] [Garagedoor] ...   │  ← status tiles
├─────────────────────────────────────────────────────────┤
│  Main Garage Door          3rd Car Door                 │  ← garage panel
├─────────────────────────────────────────────────────────┤
│  Current Readings (table)                               │
├─────────────────────────────────────────────────────────┤
│  Temperature / Heat Index / Humidity / Pressure charts  │
│  Sump pump / HVAC / Garage door history charts          │
├─────────────────────────────────────────────────────────┤
│  Summary tables (per location)                          │
└─────────────────────────────────────────────────────────┘
```

---

## Toolbar

| Control | What it does |
|---------|----------------|
| **Show Logs** | Opens a popup with recent collector activity (useful when something looks wrong). Click **Close** or outside the popup to dismiss it. |
| **Refresh now** | Reloads all data immediately instead of waiting for the next automatic refresh. |
| **Updated … · auto-refresh every 60s** | Shows when data was last loaded. The page polls for new data every **60 seconds** while the tab is open. |

If the server is unreachable, a red error banner appears at the top. Try **Refresh now** or check that you are on the home network.

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

The **Garage Door History** chart at the bottom plots both doors over time for the last 24 hours.

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

## Charts

All line charts use the **last 24 hours** of data, with one colored line per location where applicable.

| Chart | What it shows |
|-------|----------------|
| **Temperature over time** | °F by location (Attic, Garage, Inside, Outside, HVAC) |
| **Heat Index over time** | Heat index by location |
| **Humidity over time** | Relative humidity by location |
| **Pressure over time** | Barometric pressure by location |
| **Sump Pump Water Level** | Water level at the sump pump |
| **Number of Sump Pump Cycles per Day** | Bar chart — how many times the pump ran each day |
| **Number of HVAC Cycles per Day** | Bar chart — HVAC cycle counts by day |
| **Garage Door History** | Main and 3rd-car door state over 24 hours |

Hover over a chart to see exact values and timestamps. On a phone, scroll horizontally if a table or chart is wider than the screen.

---

## Summary tables

Below the charts, one table per location (**Garage**, **Inside**, **Outside**, **Attic**, **HVAC**) lists **high / low** values for:

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
| Need more detail | Click **Show Logs** and look for errors mentioning the location name. Share a screenshot with whoever maintains PiSensors. |

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
