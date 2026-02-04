from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

app = FastAPI(
    title="MediCare Hospital Management System",
    description="A comprehensive hospital management solution",
    version="2.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Main Pages
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/pharmacy", response_class=HTMLResponse)
async def pharmacy(request: Request):
    # Check if pharmacy template exists
    if os.path.exists("templates/pharmacy.html"):
        return templates.TemplateResponse("pharmacy.html", {"request": request})
    else:
        # Fallback to pharmacy-dashboard.html if exists
        if os.path.exists("static/pharmacy-dashboard.html"):
            return HTMLResponse(content=open("static/pharmacy-dashboard.html", encoding="utf-8").read())
        else:
            return templates.TemplateResponse("dashboard.html", {
                "request": request,
                "message": "Pharmacy module coming soon!"
            })

# Import API routes
try:
    from routes import dashboard as dashboard_routes, doctors, patients
    app.include_router(dashboard_routes.router, tags=["dashboard"])
    app.include_router(doctors.router, tags=["doctors"])
    app.include_router(patients.router, tags=["patients"])
    print(" All API routes loaded successfully")
except ImportError as e:
    print(f" Could not load some routes: {e}")

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print(" MEDICARE HOSPITAL MANAGEMENT SYSTEM")
    print("="*60)
    print("\n Available URLs:")
    print("    http://localhost:8000/          - Landing Page")
    print("    http://localhost:8000/dashboard - Dashboard")
    print("    http://localhost:8000/pharmacy  - Pharmacy")
    print("    http://localhost:8000/docs      - API Documentation")
    print("    http://localhost:8000/api/doctors - Doctors API")
    print("    http://localhost:8000/api/patients - Patients API")
    print("\n" + "="*60)
    print(" Server starting... Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on changes
    )
