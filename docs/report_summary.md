# report_summary

# Project Report Summary: SOLAR DAP
**Solar Irradiance Analytics, 1-Hour Ahead Machine Learning Forecasting, and Anomaly Monitoring Platform**

---

## Executive Summary

**SOLAR DAP** is an enterprise-grade, portfolio-quality solar resource analytics and forecasting platform engineered around high-resolution historical Solcast radiation and meteorological data across three geographically and climatically distinct Indian locations: **Delhi NCR**, **Jaisalmer (Rajasthan)**, and **Raipur (Chhattisgarh)**.

The initiative bridges advanced empirical solar data science with production-oriented software engineering. It transitions raw 15-minute satellite-derived atmospheric irradiance observations through rigorous exploratory data analysis (EDA), solar resource decomposition, and baseline modeling, into a validated 1-hour-ahead ($t+4$) machine learning forecasting pipeline, statistical residual anomaly monitoring, a high-throughput Python FastAPI backend service, and a responsive, dark-themed React 19 + TypeScript web application.

```
+-------------------------------------------------------------------------------------------------------+
|                                          SOLAR DAP PLATFORM                                           |
+-------------------------------------------------------------------------------------------------------+
|  [ Layer 1: Data Engineering ]   --> 15-min Solcast records (104,832 rows), IST (+05:30) normalized    |
|  [ Layer 2: Solar EDA ]          --> Irradiance decomposition (GHI/DNI/DHI/GTI), Cloud Regression     |
|  [ Layer 3: ML Forecasting ]     --> 1-Hr ($t+4$) Random Forest vs Persistence Benchmark (R² = 0.990) |
|  [ Layer 4: Anomaly Detection ]  --> City-specific 99th-percentile residual thresholding (211 flagged) |
|  [ Layer 5: Backend API ]        --> FastAPI REST service, Pydantic v2, in-memory caching             |
|  [ Layer 6: Frontend App ]       --> React 19, TypeScript, Vite, Tailwind CSS, Recharts, Lucide UI    |
+-------------------------------------------------------------------------------------------------------+
```

---

## 1. Project Background & Problem Statement

Solar photovoltaic (PV) generation is intrinsically intermittent, driven by diurnal solar geometry and dynamic atmospheric phenomena such as cloud coverage, relative humidity, aerosol optical depth, and ambient temperature. Efficient grid integration, dispatch planning, energy trading, and asset operations demand:
1. **Accurate Solar Resource Assessment:** Disaggregation of global horizontal irradiance into direct, diffuse, and plane-of-array tilted components.
2. **Short-Term Predictive Forecasting:** Multi-horizon forecasting ($15$ to $60$ minutes ahead) that substantially outperforms classical persistence assumptions.
3. **Automated Anomaly Detection:** Real-time flagging of unexplained generation drops to distinguish between meteorological attenuation (rapid cloud passage) and potential balance-of-system (BOS) failures.
4. **Professional Decision-Support Interfaces:** Low-latency, visually intuitive analytical dashboards delivering clean time-series visualization and diagnostic transparency.

SOLAR DAP addresses these requirements through an integrated, multi-tier data and software architecture.

---

## 2. Complete Technical Stack

| Tier / Domain | Technology / Library | Version | Role & Architectural Purpose |
| :--- | :--- | :--- | :--- |
| **Frontend Framework** | **React** | `^19.2.8` | Component-driven UI architecture, functional hooks, concurrent rendering |
| **Frontend Language** | **TypeScript** | `~6.0.2` | Static type safety, strict interface contracts matching backend DTO schemas |
| **Build & Tooling** | **Vite** | `^8.3.0` | Ultra-fast HMR development server, optimized ESM production builds |
| **Styling & Design System** | **Tailwind CSS** | `^3.4.19` | Utility-first CSS engine, responsive layouts, custom dark color palette |
| **UI Class Utilities** | **clsx** & **tailwind-merge** | `^2.1.1` / `^3.7.0` | Dynamic class construction and conflict-free utility merging |
| **Data Visualization** | **Recharts** | `^3.10.1` | Declarative SVG charting (Area, Composed Line, Scatter, Bar, dual Y-axis) |
| **Iconography** | **Lucide React** | `^1.54.0` | Clean, unified iconography for navigation, solar indicators, and metrics |
| **Code Quality & Linter** | **Oxlint** | `^1.81.0` | High-performance Rust-based static code analysis |
| **Backend Microservice** | **FastAPI** | `>=0.110.0` | Asynchronous ASGI REST API framework with native OpenAPI 3.0 docs |
| **ASGI Server** | **Uvicorn** | `>=0.28.0` | Lightning-fast ASGI web server implementation |
| **Data Validation** | **Pydantic** | `>=2.0.0` | Strict data validation, serialization, and typing schemas |
| **Numerical Processing** | **Pandas** & **NumPy** | `>=2.0.0` / `>=1.24.0` | Time-series slicing, rolling windows, aggregations, in-memory caching |
| **Datetime Handling** | **python-dateutil** | `>=2.8.2` | ISO-8601 parsing, UTC awareness, and timezone transformations |
| **Machine Learning** | **scikit-learn** | `>=1.4.0` | Random Forest regressors, dummy baselines, metric evaluation |
| **Model Serialization** | **Joblib** | `>=1.3.0` | Optimized model artifact persistence and disk serialization |
| **Data Science / EDA** | **Jupyter / Colab** | Python 3.12 | Exploratory data analysis, statistical regression, iterative model tuning |

---

## 3. Dataset Characteristics & Solar Domain Engineering

### 3.1 Dataset Overview
The platform processes full-year 2025 solar radiation and weather datasets acquired from Solcast for three Indian geographical benchmarks:

| Location | Latitude / Longitude | Climate Classification | Optimal Fixed Tilt | Azimuth | Observations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Delhi NCR** | $28.704^\circ\text{ N}, 77.102^\circ\text{ E}$ | Semi-Arid / Composite | $26.0^\circ$ | $180.0^\circ$ (South) | 34,944 rows |
| **Jaisalmer** | $26.909^\circ\text{ N}, 70.915^\circ\text{ E}$ | Hot Arid (Thar Desert) | $25.0^\circ$ | $180.0^\circ$ (South) | 34,944 rows |
| **Raipur** | $21.251^\circ\text{ N}, 81.630^\circ\text{ E}$ | Tropical Wet & Dry | $20.0^\circ$ | $180.0^\circ$ (South) | 34,944 rows |
| **Consolidated** | — | **3 Climatic Zones** | — | — | **104,832 rows** |

### 3.2 Atmospheric & Solar Parameters
Each 15-minute integration period captures 8 primary continuous physical variables:
- **Global Horizontal Irradiance (GHI, $\text{W/m}^2$):** Total geometric solar radiation incident on a horizontal surface.
- **Direct Normal Irradiance (DNI, $\text{W/m}^2$):** Solar beam radiation received perpendicular to the solar rays.
- **Diffuse Horizontal Irradiance (DHI, $\text{W/m}^2$):** Radiation scattered by clouds, aerosols, and atmosphere.
- **Global Tilted Irradiance (GTI, $\text{W/m}^2$):** Total radiation arriving on the plane of a fixed-tilt PV collector.
- **Air Temperature ($^\circ\text{C}$):** Ambient dry-bulb temperature measured at 2 meters.
- **Relative Humidity (%):** Ratio of vapor pressure to saturation water vapor pressure.
- **Cloud Opacity (%):** Satellite-derived optical thickness representing fractional cloud attenuation.
- **Wind Speed at 10m ($\text{m/s}$):** Atmospheric horizontal wind velocity influencing PV cell cooling.

### 3.3 Critical Domain Conventions Handled
1. **Interval-End Timestamp Semantics:** Solcast timestamps identify the **end** of each 15-minute measurement interval (`PT15M`). Consequently, daily insolation integral calculations are strictly computed as:
   $$\text{Daily Insolation } (\text{kWh/m}^2/\text{day}) = \sum_{k=1}^{96} \left( \text{GHI}_k \times 0.25 \, \text{hours} \right) \div 1000$$
2. **Timezone Normalization (IST, UTC+05:30):** The raw exports utilized longitudinal time representations with source offsets (`+05:00` for Delhi/Raipur, `+04:00` for Jaisalmer). The data loader parses all timestamps with UTC awareness and normalizes them uniformly to Indian Standard Time (`Asia/Kolkata`, `UTC+05:30`). This prevents clock-time skew and preserves observation counts ($364 \times 96 = 34,944$ intervals per city).
3. **Data Integrity:** Zero missing records and zero duplicate timestamps across all 104,832 records.

---

## 4. Phase 1: Exploratory Data Analysis & Resource Insights

Exploratory analysis established fundamental empirical baselines:

```
          SOLAR IRRADIANCE DECOMPOSITION CLOSURE
          GHI = DHI + DNI * cos(Zenith Angle)
```

1. **Diurnal Solar Progression:** Typical bell-shaped diurnal profiles peaking between 12:00 and 13:00 IST. GTI consistently exceeds GHI during winter months due to the seasonal low solar altitude and optimal southward panel tilt ($20^\circ - 26^\circ$).
2. **Empirical Cloud Opacity vs. GHI Regression:**
   - Evaluated across daylight observations ($\text{GHI} > 0$).
   - **Slope:** $-6.93 \, \text{W/m}^2$ per $1\%$ increase in cloud opacity.
   - **Intercept:** $574.54 \, \text{W/m}^2$ under clear-sky conditions.
   - **Pearson Correlation:** $r = -0.530$ ($p = 2.68 \times 10^{-25}$).
   - **Coefficient of Determination ($R^2$):** $0.281$.
   - **Interpretation:** While cloud opacity exhibits a statistically significant negative association with surface irradiance, cloud cover alone explains only $28.1\%$ of daylight GHI variance. Solar zenith angle, optical air mass, and atmospheric aerosol dispersion account for the remaining variance.
3. **Regional Comparative Insolation:**
   - **Jaisalmer:** Highest annual insolation, superior clear-sky index, minimal cloud perturbation throughout the dry seasons.
   - **Delhi NCR:** Severe attenuation in late autumn and winter driven by dense particulate matter, haze, and temperature inversions.
   - **Raipur:** Pronounced monsoon dip (June–September) characterized by persistent heavy cloud cover and high relative humidity.

---

## 5. Phase 2 & 3: Machine Learning Engineering & Forecasting

### 5.1 Architecture Evolution: Contemporaneous Estimation vs. Genuine Forecasting
Early exploration included a contemporaneous estimation model predicting current GHI from same-interval weather variables ($R^2 = 0.967$). While mathematically robust, that model assumed instantaneous knowledge of future weather. 

The project subsequently engineered a **genuine 1-hour-ahead ($t+4$ intervals) predictive forecasting pipeline** using only information strictly available at forecast creation time $t$.

### 5.2 Model Configuration & Data Splitting
- **Chronological Holdout Partitioning:** Strict time-based split at the 80th percentile of the target timestamp to guarantee zero data leakage from future observations.
  - **Training Set:** 83,846 samples (January 1, 2025 to October 19, 2025 06:00 IST)
  - **Testing Holdout:** 20,962 samples (October 19, 2025 06:15 IST to December 31, 2025 01:30 IST)
- **Model Algorithm:** Optimized `RandomForestRegressor` (`n_estimators=100`, `min_samples_leaf=3`, `random_state=42`, `n_jobs=-1`).
- **Target Variable:** $\text{GHI}_{t+4}$ (Global Horizontal Irradiance 60 minutes into the future).

### 5.3 Feature Engineering Matrix (14 Features)
1. **Autoregressive Irradiance Lags:**
   - $\text{GHI}_t$ (`ghi_now`): Current observed irradiance.
   - $\text{GHI}_{t-1}$ (`ghi_15min_ago`): 15-minute lag capturing short-term gradient.
   - $\text{GHI}_{t-4}$ (`ghi_1hr_ago`): 60-minute lag capturing diurnal slope.
2. **Exogenous Meteorological Covariates (Observed at time $t$):**
   - Air Temperature ($^\circ\text{C}$), Cloud Opacity (%), Relative Humidity (%), Wind Speed 10m (m/s).
3. **Cyclical Temporal Embeddings:**
   - Diurnal solar angle proxies: $\sin(2\pi \cdot \text{hour}/24)$, $\cos(2\pi \cdot \text{hour}/24)$ for the target hour $t+4$.
   - Annual solar declination proxies: $\sin(2\pi \cdot \text{doy}/365)$, $\cos(2\pi \cdot \text{doy}/365)$ for the target day.
4. **Spatial Categorical Encodings:**
   - One-hot binary location indicators: `location_Delhi`, `location_Jaisalmer`, `location_Raipur`.

### 5.4 Feature Importance Analysis (Gini Impurity)

```text
Feature                      Importance (%)    Cumulative Bar
-------------------------------------------------------------------------
ghi_now                          79.03 %       ████████████████████████████
target_hour_cos                  10.58 %       ████
target_hour_sin                   6.77 %       ██
cloud_opacity                     1.61 %       █
relative_humidity                 0.35 %       ▏
target_year_sin                   0.29 %       ▏
target_year_cos                   0.27 %       ▏
ghi_1hr_ago                       0.27 %       ▏
wind_speed_10m                    0.26 %       ▏
ghi_15min_ago                     0.24 %       ▏
air_temp                          0.22 %       ▏
Spatial Encodings (3 cities)      0.13 %       ▏
```
*Insight:* The autoregressive anchor `ghi_now` accounts for $79.03\%$ of predictive weight, while cyclical hour features contribute $17.35\%$, confirming that diurnal geometric bounds dominate clear-sky physics.

### 5.5 Benchmark Comparison & Test Holdout Results

The Random Forest model was rigorously evaluated against two standard baselines:
1. **Dummy Mean Baseline:** Predicts the constant mean GHI of the training set.
2. **Persistence Baseline:** Predicts future irradiance as equal to current irradiance ($\hat{y}_{t+4} = y_t$). In solar engineering, beating persistence is the gold standard of real forecast skill.

#### Overall Holdout Metrics (20,962 test observations):
| Model | MAE ($\text{W/m}^2$) | RMSE ($\text{W/m}^2$) | $R^2$ Score | Performance Assessment |
| :--- | :--- | :--- | :--- | :--- |
| **Mean Baseline** | $228.42$ | $252.04$ | $-0.028$ | Baseline failure (uninformative) |
| **Persistence Baseline** | $56.34$ | $92.50$ | $0.862$ | Standard physical benchmark |
| **Random Forest ($t+4$)** | **$10.60$** | **$25.00$** | **$0.990$** | **81.2% MAE error reduction over persistence** |

#### Location-Specific Holdout Evaluation:
| Location | Test Samples | Persistence MAE | Persistence $R^2$ | **Random Forest MAE** | **Random Forest RMSE** | **Random Forest $R^2$** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Delhi NCR** | 6,986 | $50.77 \, \text{W/m}^2$ | $0.854$ | **$12.75 \, \text{W/m}^2$** | $27.82 \, \text{W/m}^2$ | **$0.984$** |
| **Jaisalmer** | 6,990 | $60.12 \, \text{W/m}^2$ | $0.864$ | **$7.93 \, \text{W/m}^2$** | $18.96 \, \text{W/m}^2$ | **$0.995$** |
| **Raipur** | 6,986 | $58.14 \, \text{W/m}^2$ | $0.863$ | **$11.11 \, \text{W/m}^2$** | $27.24 \, \text{W/m}^2$ | **$0.989$** |

*Key Takeaway:* Jaisalmer achieved the lowest prediction error ($\text{MAE} = 7.93 \, \text{W/m}^2$, $R^2 = 0.995$) owing to low cloud volatility during the October–December test window, whereas Delhi exhibited slightly higher variance ($\text{MAE} = 12.75 \, \text{W/m}^2$) due to atmospheric pollution dynamics.

---

## 6. Phase 4: Statistical Anomaly Monitoring Framework

### 6.1 Anomaly Detection Methodology
Rather than assuming arbitrary fixed error thresholds, anomaly detection was formulated around **city-specific 99th-percentile absolute residuals** on holdout predictions:
$$\text{Residual}_t = \text{Actual GHI}_t - \text{Predicted GHI}_t$$
$$\text{Absolute Residual } |e_t| > \tau_{99, \text{city}}$$

### 6.2 Empirical Thresholds & Flagged Statistics
- **Delhi NCR Cutoff:** $\tau_{99} = 120.72 \, \text{W/m}^2$ (70 observations flagged)
- **Jaisalmer Cutoff:** $\tau_{99} = 81.46 \, \text{W/m}^2$ (71 observations flagged)
- **Raipur Cutoff:** $\tau_{99} = 136.32 \, \text{W/m}^2$ (70 observations flagged)
- **Total Flagged Anomalies:** **211 events** out of 20,962 test intervals ($1.00\%$).

### 6.3 Severity Stratification & Root-Cause Classification
- **Critical Severity ($|e_t| \ge 200.0 \, \text{W/m}^2$):** 38 high-discrepancy events. These predominantly occur during mid-day intervals (11:00–14:00 IST) when sudden localized cloud formations or rapid aerosol plumes drop measured irradiance drastically below clear-sky model projections (e.g., Jaisalmer on Dec 28: actual $230 \, \text{W/m}^2$ vs predicted $543 \, \text{W/m}^2$).
- **High Severity ($\tau_{99} \le |e_t| < 200.0 \, \text{W/m}^2$):** 173 events representing transient forecasting discrepancies.
- **Operational Caveat Maintained:** Flagged anomalies represent statistical model prediction discrepancies, not unverified physical plant hardware faults. This distinction is clearly reflected in the UI to maintain scientific integrity.

---

## 7. Backend Architecture & REST API Service

The backend is built with Python 3.12 and FastAPI, operating as an asynchronous service designed for sub-10ms response times on analytical queries.

### 7.1 Architecture & Design Highlights
- **Path-Independent Configuration:** `app/config.py` uses anchored `Path(__file__).resolve()` resolution, ensuring robustness across any execution directory.
- **In-Memory Caching:** Source CSVs and ML artifacts are loaded once and cached in memory (`_DATA_CACHE`, `_PREDICTIONS_CACHE`, `_ANOMALIES_CACHE`), eliminating repeated disk I/O.
- **Strict Pydantic Validation:** Every response adheres to typed Pydantic models with OpenAPI schema auto-generation.
- **CORS Support:** Pre-configured for Vite development ports (`5173`, `4173`, `3000`).

```
solar-dap/backend/
├── app/
│   ├── config.py           # City configurations, coordinates, tilt, timezone constants
│   ├── data_loader.py      # Solcast dataset loader, IST normalization, summary statistics
│   ├── ml_loader.py        # ML artifacts loader, filterable predictions & anomaly engine
│   ├── schemas.py          # Strict Pydantic models for request/response serialization
│   ├── main.py             # FastAPI initialization, CORS middleware, router mounts
│   └── routers/
│       ├── health.py       # GET /api/health
│       ├── analytics.py    # GET /api/analytics/cities, summary, timeseries
│       └── ml.py           # GET /api/ml/metrics, city-metrics, feature-importance, predictions, anomalies
├── requirements.txt        # Minimal production dependencies
├── test_ml_endpoints.py    # TestClient test harness verifying all 6 API endpoints
└── README.md
```

### 7.2 API Endpoints Matrix

| HTTP Method | Route | Parameters | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | None | Service liveness, dataset directory status, supported cities |
| `GET` | `/api/analytics/cities` | None | Registry of cities with coordinates, tilt angles, climate zones |
| `GET` | `/api/analytics/summary` | `location` | Annual insolation, daily averages, peak irradiance, weather summaries |
| `GET` | `/api/analytics/timeseries` | `location`, `start_date`, `end_date` | 15-minute IST time-series slices for GHI, DNI, DHI, GTI, weather |
| `GET` | `/api/ml/metrics` | None | Overall holdout metrics (Mean, Persistence, RF) and model specifications |
| `GET` | `/api/ml/city-metrics` | None | City-by-city performance comparison (RF vs Persistence) |
| `GET` | `/api/ml/feature-importance`| None | Gini feature importance rankings and percentage contributions |
| `GET` | `/api/ml/predictions` | `location`, `date`, `limit` | Actual vs Predicted vs Persistence holdout time-series data |
| `GET` | `/api/ml/anomalies` | `location`, `severity`, `limit` | Flagged 99th-percentile anomaly records with residual thresholds |

---

## 8. Frontend Architecture & User Interface Modules

The frontend is a portfolio-grade single-page application (SPA) built using React 19, TypeScript, Vite, and Tailwind CSS. It is styled with a custom dark palette (`#0B1120`, `#111C35`) accented by warm solar amber (`#F59E0B`), emerald (`#10B981`), and rose (`#F43F5E`).

```
solar-dap/frontend/src/
├── api/
│   ├── client.ts           # Centralized async fetch client with unified error handling
│   └── types.ts            # TypeScript interfaces for all backend API contracts
├── components/
│   ├── common/
│   │   ├── KpiCard.tsx     # Reusable KPI tile with iconography, units & trend badges
│   │   └── StateViews.tsx  # Graceful LoadingState, ErrorState, and EmptyState components
│   ├── layout/
│   │   ├── Header.tsx      # Top bar with location switcher, date indicator, live backend badge
│   │   └── Sidebar.tsx     # Collapsible navigation drawer with tab routing
│   └── pages/
│       ├── OverviewPage.tsx            # Executive KPI summary, diurnal curve, regional benchmarks
│       ├── SolarAnalyticsPage.tsx      # Decomposition, 7-day scrubber, cloud scatter, correlation matrix
│       ├── ForecastingPage.tsx         # Actual vs Predicted charts, city metrics, feature importance
│       ├── AnomalyMonitoringPage.tsx   # Filterable anomaly data grid, severity distribution, residuals
│       └── ModelInsightsPage.tsx       # Model architecture, error by GHI band, limitation notes
├── data/
│   └── sampleSolarData.ts  # Fallback offline constants & geographical metadata
├── types/
│   └── index.ts            # Frontend navigation and domain types
├── App.tsx                 # Layout shell, tab state, responsive layout
└── main.tsx
```

### 8.1 Module Breakdown

#### 1. Executive Overview Page
- **Regional KPI Summary Cards:** Annual Insolation ($\text{kWh/m}^2/\text{yr}$), Daylight Mean Irradiance ($\text{W/m}^2$), Peak Clear-Sky GHI ($\text{W/m}^2$), and Average Ambient Temperature ($^\circ\text{C}$).
- **Interactive 24-Hour Diurnal Profile:** High-resolution area/line chart displaying diurnal curves with toggleable DNI and DHI irradiance decomposition.
- **Cross-City Insolation Comparison:** Comparative side-by-side radiation analysis across Delhi, Jaisalmer, and Raipur.
- **7-Day Trend Scrubber:** Chronological daily insolation bar chart tracking weekly weather volatility.

#### 2. Solar Resource Analytics Page
- **Multi-Component Irradiance Decomposition:** Stacked and interactive line charts showing simultaneous progression of GHI, DNI, DHI, GTI, Cloud Opacity, and Temperature.
- **Temporal Progression Viewer:** Flexible switching between single-day 24-hour drill-down and full 7-day chronological sequences.
- **Cloud Opacity vs. GHI Scatter Analysis:** Empirical scatter plot with fitted Ordinary Least Squares (OLS) regression line and live correlation indicators.
- **Daylight Atmospheric Correlation Matrix:** Visual heatmap displaying pairwise correlations across all 8 atmospheric and irradiance features.
- **Daily Insolation Summary Table:** Tabular breakdown of daily generation potential, peak radiation, and daylight hours.

#### 3. 1-Hour Machine Learning Forecasting Page
- **Actual vs. Predicted vs. Persistence Chart:** Real-time 15-minute resolution comparison of 1-hour-ahead Random Forest predictions against ground-truth Solcast observations and persistence baselines.
- **Model Benchmark Dashboard:** Top-level metric cards highlighting the $81.2\%$ MAE reduction over persistence ($10.60 \, \text{W/m}^2$ vs $56.34 \, \text{W/m}^2$).
- **Regional Performance Breakdown Table:** City-by-city evaluation metrics showing Delhi, Jaisalmer, and Raipur validation performance.
- **Gini Feature Importance Bar Chart:** Visual ranking of top predictive drivers (`ghi_now`, `target_hour_cos`, `target_hour_sin`, `cloud_opacity`).
- **Interactive Date & City Selectors:** Allows inspection across any day in the October 19 – December 31, 2025 test holdout window.

#### 4. Statistical Anomaly Monitoring Page
- **Dynamic Residual Metric Cards:** Real-time metrics for Total Flagged Observations ($211$), Critical Discrepancies ($38$), and City-Specific 99th-percentile Thresholds ($81.5 - 136.3 \, \text{W/m}^2$).
- **Filterable Anomaly Ledger:** High-density data grid filterable by Location (All, Delhi, Jaisalmer, Raipur), Severity (All, Critical, High), and live text search.
- **Discrepancy Bar Chart:** Visualizes individual residual magnitudes against the dynamic threshold cutoff line.
- **Transparent Operational Labeling:** Explicit visual badges identifying flags as statistical model residuals rather than unconfirmed plant hardware faults.

#### 5. Model Insights & Diagnostic Evaluation Page
- **Model Architecture Specifications:** Transparent declaration of Random Forest hyperparameters, training data volume ($83,846$ rows), and test holdout parameters ($20,962$ rows).
- **Error Segmentation by Irradiance Band:** Granular evaluation table demonstrating performance across irradiance tiers ($0-50$, $50-200$, $200-400$, $400-600$, $600+ \, \text{W/m}^2$), highlighting slight positive daylight overprediction bias.
- **Limitations & Boundary Declarations:** Engineering notes documenting holdout limitations and future calibration requirements before field deployment.

---

## 9. Key Technical Achievements & Project Milestones

```
[ MILESTONES DELIVERED ]
✔ Milestone 1: Data ingestion, UTC/IST timezone normalization, interval-end alignment
✔ Milestone 2: Exploratory data analysis, decomposition closure, cloud regression analysis
✔ Milestone 3: Contemporaneous baseline vs Dummy regressor evaluation
✔ Milestone 4: Non-leaking 1-hour ($t+4$) ML forecasting pipeline exceeding persistence
✔ Milestone 5: City-specific 99th-percentile residual anomaly detection & classification
✔ Milestone 6: High-throughput FastAPI REST backend with in-memory caching & full test suite
✔ Milestone 7: Portfolio-grade React 19 + TypeScript + Tailwind CSS analytics web application
```

1. **Demonstrated Forecast Superiority:** Slashed 1-hour forecasting MAE from $56.34 \, \text{W/m}^2$ (persistence baseline) to **$10.60 \, \text{W/m}^2$** (Random Forest), lifting $R^2$ from $0.862$ to **$0.990$**.
2. **Domain-Compliant Data Engineering:** Correctly resolved Solcast interval-end integration semantics and longitudinal offsets to Indian Standard Time without data loss or timestamp distortion.
3. **End-to-End Cohesive System:** Built a completely decoupled, modular architecture connecting raw CSV files to a Python analytical service and an interactive web frontend.
4. **Honest Scientific Reporting:** Clearly differentiated between contemporaneous weather estimation models, genuine future forecasting models, and statistical model residuals vs physical hardware anomalies.

---

## 10. Future Roadmap & Planned Extensions

1. **Multi-Horizon Deep Learning Models:** Implement Temporal Fusion Transformers (TFT), N-BEATS, or PatchTST for multi-step recursive forecasting ($t+1$ through $t+24$, spanning 15 minutes to 6 hours ahead).
2. **Satellite Cloud Motion Vectors:** Incorporate real-time INSAT-3D / satellite cloud vector tracking to anticipate rapid convective cloud transitions before ground sensors register irradiance drops.
3. **Live Telemetry & Inverter PV Yield Modeling:** Couple irradiance forecasts with PVsyst-equivalent physical module equations (considering temperature coefficients, inverter clipping, and soiling losses) to predict AC kilowatt-hour generation directly.
4. **Automated Anomaly Root-Cause Classification:** Integrate unsupervised clustering (e.g., Isolation Forests, DBSCAN) to automatically categorize anomalies into cloud transients, pyranometer calibration drift, or soiling events.
5. **Containerization & Cloud CI/CD:** Package the FastAPI backend and Vite frontend into multi-stage Docker containers with automated GitHub Actions testing and deployment to cloud infrastructure (e.g., GCP Cloud Run / AWS ECS).

---

*Report generated for SOLAR DAP project documentation. Maintained in `docs/report_summary.md`.*
