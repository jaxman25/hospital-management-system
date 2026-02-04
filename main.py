from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html from root
@app.get("/")
async def read_root():
    return FileResponse("index.html")

# Serve hospital_navigation.html
@app.get("/hospital_navigation")
async def get_navigation():
    return FileResponse("hospital_navigation.html")

# Import your routes
try:
    from routes import dashboard, doctors, patients
    app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
    app.include_router(doctors.router, prefix="/api/doctors", tags=["doctors"])
    app.include_router(patients.router, prefix="/api/patients", tags=["patients"])
    print("All routes loaded successfully")
except ImportError as e:
    print(f"Could not load some routes: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
