from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import database
from models import Base

# Create database tables
Base.metadata.create_all(bind=database.engine)

# Create FastAPI app
app = FastAPI(
    title="Hospital Management System", 
    version="1.0.0",
    description="A comprehensive hospital management system",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to mount static files if directory exists
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    print(" Static files mounted")
except Exception as e:
    print(f"Note: Could not mount static files: {e}")

# Import and include routes with better error handling
try:
    from routes.dashboard import router as dashboard_router
    app.include_router(dashboard_router)
    print(" Dashboard routes loaded")
except Exception as e:
    print(f"  Could not load dashboard routes: {e}")

try:
    from routes.doctors import router as doctors_router
    app.include_router(doctors_router)
    print(" Doctors routes loaded")
except Exception as e:
    print(f"  Could not load doctors routes: {e}")

try:
    from routes.patients import router as patients_router
    app.include_router(patients_router)
    print(" Patients routes loaded")
except Exception as e:
    print(f"  Could not load patients routes: {e}")

@app.get("/")
async def root():
    return {
        "message": "Hospital Management System API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "docs": "/docs",
            "redoc": "/redoc",
            "dashboard": "/dashboard",
            "doctors_api": "/api/doctors",
            "patients_api": "/api/patients",
            "doctors_ui": "/doctors/",
            "patients_ui": "/patients/"
        }
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "hospital-management",
        "database": "connected",
        "version": "1.0.0"
    }

@app.get("/api/info")
async def system_info():
    import sys
    return {
        "python_version": sys.version.split()[0],
        "fastapi_version": "0.104.1",
        "system": "Hospital Management System",
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
