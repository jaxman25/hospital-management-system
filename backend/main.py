from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

# Import API routers
from backend.api import patients, doctors, appointments

# Create database tables
from backend.database import Base, engine
from backend.models import *
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Hospital Management System",
    version="1.0.0",
    description="A comprehensive hospital management system built with FastAPI",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "hospital-management",
        "database": "connected",
        "version": "1.0.0"
    }

# Root endpoint - Dashboard
@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hospital Management Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 40px; }
            .header h1 { color: #2c3e50; }
            .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .card h3 { color: #3498db; margin-top: 0; }
            .btn { display: inline-block; background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px; }
            .btn:hover { background: #2980b9; }
            .btn-secondary { background: #95a5a6; }
            .btn-secondary:hover { background: #7f8c8d; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1> Hospital Management System</h1>
                <p>Welcome to the Hospital Management Dashboard</p>
            </div>
            
            <div class="cards">
                <div class="card">
                    <h3> Doctors Management</h3>
                    <p>Manage doctors, specialties, and schedules</p>
                    <a href="/docs#/doctors" class="btn" target="_blank">Manage Doctors via API</a>
                </div>
                
                <div class="card">
                    <h3> Patients Management</h3>
                    <p>Patient records, medical history, and registration</p>
                    <a href="/docs#/patients" class="btn" target="_blank">Manage Patients via API</a>
                </div>
                
                <div class="card">
                    <h3> Appointments</h3>
                    <p>Schedule and manage patient appointments</p>
                    <a href="/docs#/appointments" class="btn" target="_blank">Manage Appointments via API</a>
                </div>
                
                <div class="card">
                    <h3> API Documentation</h3>
                    <p>Interactive API documentation with Swagger UI</p>
                    <a href="/docs" class="btn" target="_blank">Open API Docs</a>
                </div>
                
                <div class="card">
                    <h3> System Health</h3>
                    <p>Check system status and database connection</p>
                    <a href="/api/health" class="btn btn-secondary">Health Check</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Serve static files if they exist
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
