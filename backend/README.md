# SOLAR DAP — FastAPI Backend Service

This directory contains the Python FastAPI backend service for **SOLAR DAP**, providing historical solar irradiance and weather analytics for Delhi NCR, Jaisalmer, and Raipur.

---

## 1. Prerequisites

- Python 3.10+ (tested on Python 3.12)
- Windows PowerShell or command shell

---

## 2. Setup & Installation (Windows PowerShell)

Open PowerShell and navigate to the `backend/` directory:

```powershell
cd d:\solar-dap\backend
```

Install the required Python dependencies:

```powershell
pip install -r requirements.txt
```

---

## 3. Running the Server

### Option 1: Unified Launcher (Serves Frontend UI + Backend API)
From the project root:
```powershell
python run.py
```

### Option 2: Direct Uvicorn Command
From this `backend/` directory:
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at:
- **Web Dashboard:** `http://localhost:8000` (or `http://127.0.0.1:8000`)
- **API Base URL:** `http://localhost:8000/api`
- **Interactive OpenAPI Docs:** `http://localhost:8000/docs`
- **Alternative Redoc:** `http://localhost:8000/redoc`

### CORS & Proxy Support
- When running through FastAPI on port 8000, the frontend and API share the exact same origin, guaranteeing zero CORS issues.
- In development mode (Vite at `http://localhost:5173`), Vite's dev server proxies `/api` directly to `http://127.0.0.1:8000`.
- FastAPI's `CORSMiddleware` is configured to allow all dev origins (`localhost`, `127.0.0.1`, `*`) with full method and header support.

---

## 4. Available Endpoints

### 1. Health Check
* **Route:** `GET /api/health`
* **Description:** Verifies service status, dataset directory availability, and supported cities.

### 2. Available Cities & Metadata
* **Route:** `GET /api/analytics/cities`
* **Description:** Returns registry of available cities with coordinates, tilt angles, climate zones, and source offsets.

### 3. Historical Summary Statistics
* **Route:** `GET /api/analytics/summary?location={city}`
* **Example:** `http://localhost:8000/api/analytics/summary?location=Delhi`
* **Description:** Returns annual insolation totals, peak/daylight irradiance metrics (GHI, DNI, DHI, GTI), and weather statistics (temperature, humidity, cloud opacity, wind).

### 4. 15-Minute Time-Series Slices
* **Route:** `GET /api/analytics/timeseries?location={city}&start_date={YYYY-MM-DD}&end_date={YYYY-MM-DD}`
* **Example:** `http://localhost:8000/api/analytics/timeseries?location=Delhi&start_date=2025-06-01&end_date=2025-06-07`
* **Description:** Returns 15-minute observations normalized to Indian Standard Time (IST, `Asia/Kolkata`) for charting.

---

## 5. Dataset & Timezone Conventions

1. **Path Resolution:** The application resolves the dataset path relative to `app/config.py`, meaning it is independent of the shell working directory.
2. **Interval-End Convention:** Solcast timestamps mark the end of the 15-minute integration period.
3. **Timezone Normalization:** Original longitudinal offsets (`+05:00` for Delhi and Raipur, `+04:00` for Jaisalmer) are parsed as UTC-aware datetimes and normalized to `Asia/Kolkata` (`UTC+05:30`) without altering observation counts.
