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

    # Fallback if frontend is not built
    return {
        "service": "SOLAR DAP Analytics API",
        "version": "0.1.0",
        "documentation": "/docs",
        "health_check": "/api/health",
        "status": "online",
        "notice": "Frontend build not detected at frontend/dist. Run 'npm run build' in frontend directory to serve UI through FastAPI."
    }

