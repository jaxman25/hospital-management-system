from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# Create FastAPI app
app = FastAPI(
    title="Hospital Management System",
    version="1.0.0",
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

# ========== SIMPLE ENDPOINTS ==========

@app.get("/")
async def root():
    return {
        "message": "Hospital Management System API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "docs": "/docs",
            "doctors": "/api/doctors",
            "patients": "/api/patients",
            "dashboard": "/dashboard"
        }
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "hospital-management",
        "version": "1.0.0"
    }

# Simple in-memory data storage
doctors_db = [
    {"id": "1", "name": "Dr. Sarah Wilson", "specialization": "Cardiology", "contact": "123-456-7890"},
    {"id": "2", "name": "Dr. Michael Brown", "specialization": "Pediatrics", "contact": "123-456-7891"}
]

patients_db = [
    {"id": "1", "name": "John Doe", "age": 45, "gender": "Male", "condition": "Hypertension"},
    {"id": "2", "name": "Jane Smith", "age": 32, "gender": "Female", "condition": "Diabetes"}
]

# Doctors endpoints
@app.get("/api/doctors")
async def get_doctors():
    return doctors_db

@app.get("/api/doctors/{doctor_id}")
async def get_doctor(doctor_id: str):
    for doctor in doctors_db:
        if doctor["id"] == doctor_id:
            return doctor
    return {"error": "Doctor not found"}

@app.post("/api/doctors")
async def create_doctor(doctor: dict):
    doctor["id"] = str(len(doctors_db) + 1)
    doctors_db.append(doctor)
    return doctor

# Patients endpoints
@app.get("/api/patients")
async def get_patients():
    return patients_db

@app.get("/api/patients/{patient_id}")
async def get_patient(patient_id: str):
    for patient in patients_db:
        if patient["id"] == patient_id:
            return patient
    return {"error": "Patient not found"}

@app.post("/api/patients")
async def create_patient(patient: dict):
    patient["id"] = str(len(patients_db) + 1)
    patients_db.append(patient)
    return patient

# Dashboard
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title> Hospital Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f2f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 40px; }
            .header h1 { color: #2c3e50; }
            .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .card h3 { color: #3498db; margin-top: 0; }
            .btn { display: inline-block; background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px; }
            .btn:hover { background: #2980b9; }
            .stats { display: flex; justify-content: space-around; margin: 30px 0; }
            .stat { text-align: center; }
            .stat-number { font-size: 2em; color: #2c3e50; font-weight: bold; }
            .stat-label { color: #7f8c8d; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1> Hospital Management System</h1>
                <p>Welcome to the Hospital Dashboard</p>
            </div>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">''' + str(len(doctors_db)) + '''</div>
                    <div class="stat-label">Doctors</div>
                </div>
                <div class="stat">
                    <div class="stat-number">''' + str(len(patients_db)) + '''</div>
                    <div class="stat-label">Patients</div>
                </div>
                <div class="stat">
                    <div class="stat-number">0</div>
                    <div class="stat-label">Appointments Today</div>
                </div>
            </div>
            
            <div class="cards">
                <div class="card">
                    <h3> Doctors Management</h3>
                    <p>View and manage doctors</p>
                    <a href="/api/doctors" class="btn">View Doctors</a>
                    <a href="/docs#/default/create_doctor_api_doctors_post" class="btn" target="_blank">Add Doctor</a>
                </div>
                
                <div class="card">
                    <h3> Patients Management</h3>
                    <p>View and manage patients</p>
                    <a href="/api/patients" class="btn">View Patients</a>
                    <a href="/docs#/default/create_patient_api_patients_post" class="btn" target="_blank">Add Patient</a>
                </div>
                
                <div class="card">
                    <h3> API Documentation</h3>
                    <p>Interactive API documentation</p>
                    <a href="/docs" class="btn" target="_blank">Open API Docs</a>
                </div>
                
                <div class="card">
                    <h3> System Health</h3>
                    <p>Check system status</p>
                    <a href="/api/health" class="btn">Health Check</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
