# SOLAR DAP — Solar Irradiance Analytics Platform

**SOLAR DAP** is a solar irradiance analytics and forecasting platform built around historical Solcast radiation and weather data across three Indian locations: **Delhi NCR**, **Raipur**, and **Jaisalmer**.

---

## 1. Project Progress & Architecture

- [x] **Layer 1: Data Preparation & Exploratory Analysis (EDA)** — Solcast 15-minute radiation data parsed, missing values/duplicates verified, daylight correlation and cloud opacity regression analyzed.
- [x] **Layer 2: Contemporaneous Baseline Modeling** — Random Forest regressor evaluated ($R^2 = 0.967$, MAE $23.64 \, \text{W/m}^2$) against mean baseline.
- [x] **Layer 3: Frontend Shell & Overview Module (Milestones 1A & 1B)** — React + TypeScript + Vite application shell with dark theme, collapsible navigation, regional KPIs, 24-hour diurnal profile with DNI/DHI decomposition, multi-city comparison, and 7-day insolation trends.
- [x] **Layer 4: Solar Resource Analytics Module (Milestone 2)** — Multi-series irradiance decomposition (GHI, DNI, DHI, GTI), 7-day chronological progression viewer, cloud opacity vs. GHI linear regression ($r = -0.530$, $R^2 = 0.281$), daylight correlation heatmap, and daily insolation summary table.
- [ ] **Layer 5: Genuine 1-Hour-Ahead Forecasting (Milestone 3)** — $t+4$ horizon ML model benchmarked against persistence baseline.
- [ ] **Layer 6: Anomaly Monitoring & API Integration (Milestones 4 & 5)** — Residual tracking, severity classification, and model serving.

---

## 2. Directory Structure

```text
solar-dap/
├── backend/                        # Python FastAPI backend service
│   ├── app/
│   │   ├── config.py               # Robust path resolution & city configurations
│   │   ├── data_loader.py          # Solcast CSV loading, IST normalization & statistics
│   │   ├── schemas.py              # Pydantic schemas for API endpoints
│   │   ├── main.py                 # FastAPI app & CORS middleware
│   │   └── routers/
│   │       ├── health.py           # /api/health
│   │       └── analytics.py        # /api/analytics/cities, summary, timeseries
│   ├── requirements.txt
│   └── README.md
├── data/                           # Three original Solcast CSVs (Delhi, Raipur, Jaisalmer)
├── docs/
│   └── project_context.md          # Project context, dataset specifics & specifications
├── frontend/                       # React + TypeScript + Vite + Tailwind CSS frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/             # Reusable UI primitives (KpiCard, etc.)
│   │   │   ├── layout/             # Sidebar, Header
│   │   │   └── pages/              # Overview, Analytics, Forecasting, Anomaly, Insights
│   │   ├── data/                   # Representative Solcast sample datasets
│   │   ├── types/                  # TypeScript interface definitions
│   │   ├── App.tsx                 # Main layout & tab routing
│   │   └── main.tsx
│   ├── tailwind.config.js          # Dark navy/charcoal foundation + solar accent tokens
│   └── package.json
├── ml/
│   └── artifacts/                  # Exported models, predictions & metrics
└── README.md
```

---

## 3. Running the Project

### A. Quickest Option: Unified FastAPI Runner (Zero CORS)
Run the entire platform (both the React frontend UI and FastAPI REST backend) through FastAPI on a single port:
```powershell
python run.py
```
- **Unified Web Dashboard:** `http://localhost:8000` (or `http://127.0.0.1:8000`)
- **Interactive Swagger Docs:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/api/health`

*Note:* Because the frontend and backend are served together under the same origin, browser CORS restrictions are completely eliminated.

---

### B. Development Mode (Vite Dev Server + FastAPI with Proxy)
If developing the frontend with instant hot-module replacement (HMR):

1. **Option 1: One-command dual start**
```powershell
python run.py --dev
```

2. **Option 2: Separate terminals**
- **Terminal 1 (Backend):**
  ```powershell
  cd backend
  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```
- **Terminal 2 (Frontend):**
  ```powershell
  cd frontend
  npm run dev
  ```
- Vite dev server runs at `http://localhost:5173` and automatically proxies `/api` calls to `http://127.0.0.1:8000`.
- FastAPI's robust CORS middleware also permits direct cross-origin requests from `localhost:5173`, `127.0.0.1:5173`, and all local dev ports.

---

## 4. Key Dataset & Analytical Semantics

1. **15-Minute Resolution & Interval-End Convention**: Timestamps represent the end of each integration period. Daily insolation is computed as $\sum (\text{GHI} \times 0.25 \, \text{h})$.
2. **Timezone Normalization**: Longitudinal Solcast offsets (`+05:00` for Delhi/Raipur, `+04:00` for Jaisalmer) are normalized to Indian Standard Time (`Asia/Kolkata`, `UTC+05:30`).
3. **Estimation vs. Forecasting**: Contemporaneous estimation models (utilizing same-period weather inputs) are clearly separated from genuine future predictive models ($t+4$).
