from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import health, analytics, ml
from app.config import PROJECT_ROOT

app = FastAPI(
    title="SOLAR DAP — Solar Irradiance Analytics API",
    description=(
        "Backend REST API for SOLAR DAP: historical solar resource analytics, "
        "irradiance decomposition (GHI, DNI, DHI, GTI), 1-hour ML forecasting evaluation, "
        "and residual anomaly monitoring for Delhi, Raipur, and Jaisalmer."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Robust CORS middleware: handles local development (Vite, React, custom ports) and cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*",
    ],
    allow_origin_regex=r"^https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Fail-safe CORS middleware: guarantees CORS headers are present on all responses, including exceptions & errors
@app.middleware("http")
async def ensure_cors_headers(request, call_next):
    origin = request.headers.get("origin", "*")
    if request.method == "OPTIONS":
        from fastapi.responses import Response
        res = Response(content="OK", status_code=200)
    else:
        try:
            res = await call_next(request)
        except Exception as e:
            from fastapi.responses import JSONResponse
            res = JSONResponse(
                status_code=500,
                content={"detail": f"Internal Server Error: {str(e)}"}
            )
    
    if origin and origin != "*":
        res.headers["Access-Control-Allow-Origin"] = origin
        res.headers["Access-Control-Allow-Credentials"] = "true"
    else:
        res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    res.headers["Access-Control-Allow-Headers"] = "*"
    return res

# Mount API routers under /api
app.include_router(health.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(ml.router, prefix="/api")

@app.get("/api", tags=["Root"])
def api_root():
    return {
        "service": "SOLAR DAP Analytics API",
        "version": "0.1.0",
        "documentation": "/docs",
        "health_check": "/api/health",
        "status": "online"
    }

# Frontend static build paths
FRONTEND_DIST_DIR = PROJECT_ROOT / "frontend" / "dist"
ASSETS_DIR = FRONTEND_DIST_DIR / "assets"

if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

@app.get("/{full_path:path}", include_in_schema=False)
def serve_spa(full_path: str = ""):
    # Do not intercept API, OpenAPI or documentation routes
    if (
        full_path.startswith("api") 
        or full_path.startswith("docs") 
        or full_path.startswith("redoc") 
        or full_path == "openapi.json"
    ):
        raise HTTPException(status_code=404, detail=f"API endpoint not found: /{full_path}")

    # Check for direct static file in frontend/dist (e.g. favicon.svg, icons.svg)
    if full_path:
        file_path = FRONTEND_DIST_DIR / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))

    # Return React SPA index.html for root and client-side routes
    index_file = FRONTEND_DIST_DIR / "index.html"
    if index_file.is_file():
        return FileResponse(str(index_file))

    # When deployed as a standalone API backend (e.g. Render with frontend on Vercel)
    return {
        "service": "SOLAR DAP Analytics API",
        "version": "0.1.0",
        "status": "online",
        "documentation": "/docs",
        "health_check": "/api/health",
        "endpoints": {
            "cities": "/api/analytics/cities",
            "summary": "/api/analytics/summary?location=Delhi",
            "timeseries": "/api/analytics/timeseries?location=Delhi&start_date=2025-06-01&end_date=2025-06-07",
            "ml_metrics": "/api/ml/metrics",
            "city_metrics": "/api/ml/city-metrics",
            "predictions": "/api/ml/predictions?location=Delhi",
            "anomalies": "/api/ml/anomalies?location=Delhi"
        }
    }

