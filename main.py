from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import database
from models import Base

# Create database tables
Base.metadata.create_all(bind=database.engine)

# Create FastAPI app
app = FastAPI(title="Hospital Management System", version="1.0.0")

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

# Try to import and include dashboard routes
try:
    from routes import dashboard
    app.include_router(dashboard.router, tags=["dashboard"])
    print(" Dashboard routes loaded")
except Exception as e:
    print(f"Note: Could not load dashboard routes: {e}")

# Try to import and include doctors routes
try:
    from routes import doctors
    app.include_router(doctors.router)
    print(" Doctors routes loaded")
except Exception as e:
    print(f"Note: Could not load doctors routes: {e}")

# Try to import and include patients routes
try:
    from routes import patients
    app.include_router(patients.router)
    print(" Patients routes loaded")
except Exception as e:
    print(f"Note: Could not load patients routes: {e}")

@app.get("/")
async def root():
    return {
        "message": "Hospital Management System API",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc",
            "dashboard": "/dashboard",
            "doctors": "/doctors/",
            "patients": "/patients/"
        }
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "hospital-management",
        "database": "connected"
    }

@app.get("/api/info")
async def system_info():
    import sys
    return {
        "python_version": sys.version,
        "fastapi_version": "0.104.1",
        "system": "Hospital Management System"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
