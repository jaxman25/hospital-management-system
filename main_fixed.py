from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
import os

# Import database and models
from backend.database import SessionLocal, engine, Base
from backend.models import Patient, Doctor, Appointment

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

# ========== API ENDPOINTS ==========

# Health check
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "hospital-management",
        "database": "connected",
        "version": "1.0.0"
    }

# Patients endpoints
@app.get("/api/patients")
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return patients

@app.get("/api/patients/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/api/patients")
def create_patient(patient_data: dict, db: Session = Depends(get_db)):
    # Simple patient creation - in real app, use Pydantic models
    db_patient = Patient(**patient_data)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# Doctors endpoints
@app.get("/api/doctors")
def get_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = db.query(Doctor).offset(skip).limit(limit).all()
    return doctors

@app.get("/api/doctors/{doctor_id}")
def get_doctor(doctor_id: str, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.post("/api/doctors")
def create_doctor(doctor_data: dict, db: Session = Depends(get_db)):
    db_doctor = Doctor(**doctor_data)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

# Appointments endpoints
@app.get("/api/appointments")
def get_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).offset(skip).limit(limit).all()
    return appointments

@app.post("/api/appointments")
def create_appointment(appointment_data: dict, db: Session = Depends(get_db)):
    db_appointment = Appointment(**appointment_data)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

# ========== WEB PAGES ==========

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title> Hospital Management System</title>
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
            .status { padding: 10px; background: #d4edda; color: #155724; border-radius: 5px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1> Hospital Management System</h1>
                <p>FastAPI-based Hospital Management Platform</p>
            </div>
            
            <div class="status"> System Status: Online</div>
            
            <div class="cards">
                <div class="card">
                    <h3> Dashboard</h3>
                    <p>System overview and statistics</p>
                    <a href="/docs" class="btn">API Documentation</a>
                </div>
                
                <div class="card">
                    <h3> Doctors</h3>
                    <p>Manage doctors and schedules</p>
                    <a href="/api/doctors" class="btn">View Doctors API</a>
                </div>
                
                <div class="card">
                    <h3> Patients</h3>
                    <p>Patient records and management</p>
                    <a href="/api/patients" class="btn">View Patients API</a>
                </div>
                
                <div class="card">
                    <h3> Appointments</h3>
                    <p>Appointment scheduling</p>
                    <a href="/api/appointments" class="btn">View Appointments API</a>
                </div>
                
                <div class="card">
                    <h3> Health Check</h3>
                    <p>System health status</p>
                    <a href="/api/health" class="btn">Check System Health</a>
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
