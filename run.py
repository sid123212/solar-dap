"""
SOLAR DAP - Platform Runner
Unified launcher for the FastAPI backend and frontend dashboard.

Usage:
  python run.py             # Runs unified FastAPI server (Frontend UI + Backend API on port 8000)
  python run.py --dev       # Runs FastAPI backend (port 8000) and Vite dev server (port 5173) concurrently
  python run.py --port 8080 # Custom port
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

# Resolve directory locations
CURRENT_DIR = Path(__file__).resolve().parent
if (CURRENT_DIR / "solar-dap").exists():
    SOLAR_DAP_DIR = CURRENT_DIR / "solar-dap"
else:
    SOLAR_DAP_DIR = CURRENT_DIR

BACKEND_DIR = SOLAR_DAP_DIR / "backend"
FRONTEND_DIR = SOLAR_DAP_DIR / "frontend"
FRONTEND_DIST = FRONTEND_DIR / "dist"

# Add backend directory to Python module search path
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

def build_frontend_if_needed():
    """Ensure frontend build exists so FastAPI can serve the dashboard."""
    if not (FRONTEND_DIST / "index.html").exists():
        print("[SOLAR DAP] Frontend build not found in frontend/dist.")
        print("[SOLAR DAP] Building frontend with Vite...")
        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
        try:
            subprocess.run([npm_cmd, "run", "build"], cwd=str(FRONTEND_DIR), check=True)
            print("[SOLAR DAP] Frontend built successfully!")
        except Exception as e:
            print(f"[SOLAR DAP] Warning: Failed to automatically build frontend: {e}")
            print("[SOLAR DAP] You can build it manually: cd frontend && npm run build")

def main():
    parser = argparse.ArgumentParser(description="Run SOLAR DAP using FastAPI")
    parser.add_argument("--host", default="0.0.0.0", help="Host address (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--reload", action="store_true", default=True, help="Enable auto-reload on code change")
    parser.add_argument("--no-reload", action="store_false", dest="reload", help="Disable auto-reload")
    parser.add_argument("--dev", action="store_true", help="Run in dev mode (FastAPI backend + Vite dev server concurrently)")
    args = parser.parse_args()

    # Change working directory to backend so relative pathing is seamless
    os.chdir(str(BACKEND_DIR))

    if args.dev:
        print("=" * 60)
        print(" SOLAR DAP - Development Mode")
        print("=" * 60)
        print(" Starting Vite dev server (port 5173 with proxy -> 8000)")
        print(" Starting FastAPI backend (port 8000)")
        print(" No CORS errors will occur thanks to Vite reverse proxy and FastAPI CORS middleware.")
        print("=" * 60)
        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
        vite_proc = subprocess.Popen([npm_cmd, "run", "dev"], cwd=str(FRONTEND_DIR))
        try:
            import uvicorn
            uvicorn.run("app.main:app", host=args.host, port=args.port, reload=args.reload)
        finally:
            vite_proc.terminate()
        return

    # Unified mode: FastAPI serves both API and React UI
    build_frontend_if_needed()

    print("=" * 65)
    print(" SOLAR DAP — Solar Irradiance Analytics Platform")
    print("=" * 65)
    print(f" Web Dashboard:  http://localhost:{args.port}  (or http://127.0.0.1:{args.port})")
    print(f" API Docs:       http://localhost:{args.port}/docs")
    print(f" Health Check:   http://localhost:{args.port}/api/health")
    print(f" Host Binding:   {args.host}:{args.port}")
    print("-" * 65)
    print(" Frontend & Backend unified on the same server — ZERO CORS errors!")
    print("=" * 65)

    import uvicorn
    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=args.reload)

if __name__ == "__main__":
    main()
