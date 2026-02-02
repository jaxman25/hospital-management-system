from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uvicorn
from datetime import datetime, date, timedelta
from contextlib import asynccontextmanager
from typing import List, Optional
import models
from database import engine, SessionLocal
import uuid
import json

# Create all tables
models.Base.metadata.create_all(bind=engine)

# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(" Hospital Management System API Starting...")
    
    # Create sample data
    db = SessionLocal()
    try:
        # Check and create sample data if needed
        from sqlalchemy import text
        
        # Create sample doctor
        if db.query(models.Doctor).count() == 0:
            print(" Creating sample doctors...")
            
            doctors_data = [
                {
                    "first_name": "John",
                    "last_name": "Smith",
                    "license_number": "DOC001",
                    "specialization": "Cardiology",
                    "department": "Heart Center",
                    "consultation_fee": 150.0,
                    "qualifications": ["MD", "FACC"],
                    "available_days": ["Monday", "Wednesday", "Friday"],
                    "available_hours": {"start": "09:00", "end": "17:00"}
                },
                {
                    "first_name": "Sarah",
                    "last_name": "Johnson",
                    "license_number": "DOC002",
                    "specialization": "Pediatrics",
                    "department": "Children's Hospital",
                    "consultation_fee": 120.0,
                    "qualifications": ["MD", "FAAP"],
                    "available_days": ["Tuesday", "Thursday", "Saturday"],
                    "available_hours": {"start": "10:00", "end": "18:00"}
                }
            ]
            
            for doc_data in doctors_data:
                doctor = models.Doctor(
                    id=str(uuid.uuid4()),
                    first_name=doc_data["first_name"],
                    last_name=doc_data["last_name"],
                    license_number=doc_data["license_number"],
                    specialization=doc_data["specialization"],
                    department=doc_data["department"],
                    consultation_fee=doc_data["consultation_fee"],
                    qualifications=json.dumps(doc_data["qualifications"]),
                    available_days=json.dumps(doc_data["available_days"]),
                    available_hours=json.dumps(doc_data["available_hours"]),
                    is_available=True
                )
                db.add(doctor)
            
            db.commit()
            print(" Sample doctors created!")
            
    except Exception as e:
        print(f"  Could not create sample data: {e}")
    finally:
        db.close()
    
    yield
    
    # Shutdown
    print(" Hospital Management System API Shutting Down...")

# Create FastAPI app
app = FastAPI(
    title=" Hospital Management System API",
    version="1.0.0",
    description="Comprehensive Hospital Management System",
    lifespan=lifespan
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== UTILITY FUNCTIONS ====================

def generate_mrn():
    return f"MRN-{uuid.uuid4().hex[:8].upper()}"

def generate_appointment_number():
    return f"APT-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"

def generate_bill_number():
    return f"BILL-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"

# ==================== ROUTES ====================

@app.get("/")
async def root():
    return {
        "message": "Welcome to Hospital Management System API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "patients": "/api/patients",
            "doctors": "/api/doctors",
            "appointments": "/api/appointments"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "hospital-management-api",
        "database": "connected"
    }

# ==================== PATIENT ENDPOINTS ====================

@app.get("/api/patients")
async def get_patients(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get list of patients"""
    query = db.query(models.Patient)
    if active_only:
        query = query.filter(models.Patient.is_active == True)
    
    patients = query.offset(skip).limit(limit).all()
    return {
        "count": len(patients),
        "patients": [p.to_dict() for p in patients]
    }

@app.get("/api/patients/{patient_id}")
async def get_patient(patient_id: str, db: Session = Depends(get_db)):
    """Get specific patient by ID"""
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient.to_dict()

@app.post("/api/patients")
async def create_patient(
    first_name: str,
    last_name: str,
    date_of_birth: str,
    contact_number: str,
    email: Optional[str] = None,
    gender: Optional[str] = None,
    blood_group: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a new patient"""
    try:
        # Parse date
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
        
        # Create patient
        patient = models.Patient(
            id=str(uuid.uuid4()),
            mrn=generate_mrn(),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=dob,
            gender=gender,
            blood_group=blood_group,
            contact_number=contact_number,
            email=email,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_active=True
        )
        
        db.add(patient)
        db.commit()
        db.refresh(patient)
        
        return {
            "message": "Patient created successfully",
            "patient_id": patient.id,
            "mrn": patient.mrn,
            "patient": patient.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating patient: {str(e)}")

@app.put("/api/patients/{patient_id}")
async def update_patient(
    patient_id: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    contact_number: Optional[str] = None,
    email: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Update patient information"""
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    try:
        if first_name:
            patient.first_name = first_name
        if last_name:
            patient.last_name = last_name
        if contact_number:
            patient.contact_number = contact_number
        if email:
            patient.email = email
        if is_active is not None:
            patient.is_active = is_active
        
        patient.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(patient)
        
        return {
            "message": "Patient updated successfully",
            "patient": patient.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating patient: {str(e)}")

# ==================== DOCTOR ENDPOINTS ====================

@app.get("/api/doctors")
async def get_doctors(
    skip: int = 0,
    limit: int = 100,
    available_only: bool = False,
    specialization: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of doctors"""
    query = db.query(models.Doctor)
    
    if available_only:
        query = query.filter(models.Doctor.is_available == True)
    
    if specialization:
        query = query.filter(models.Doctor.specialization.ilike(f"%{specialization}%"))
    
    doctors = query.offset(skip).limit(limit).all()
    return {
        "count": len(doctors),
        "doctors": [d.to_dict() for d in doctors]
    }

@app.get("/api/doctors/{doctor_id}")
async def get_doctor(doctor_id: str, db: Session = Depends(get_db)):
    """Get specific doctor by ID"""
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor.to_dict()

@app.post("/api/doctors")
async def create_doctor(
    first_name: str,
    last_name: str,
    license_number: str,
    specialization: str,
    department: Optional[str] = None,
    consultation_fee: float = 0.0,
    is_available: bool = True,
    db: Session = Depends(get_db)
):
    """Create a new doctor"""
    try:
        # Check if license number already exists
        existing = db.query(models.Doctor).filter(
            models.Doctor.license_number == license_number
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="License number already exists")
        
        # Create doctor
        doctor = models.Doctor(
            id=str(uuid.uuid4()),
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
            specialization=specialization,
            department=department,
            consultation_fee=consultation_fee,
            is_available=is_available,
            created_at=datetime.utcnow()
        )
        
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
        
        return {
            "message": "Doctor created successfully",
            "doctor_id": doctor.id,
            "doctor": doctor.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating doctor: {str(e)}")

# ==================== APPOINTMENT ENDPOINTS ====================

@app.get("/api/appointments")
async def get_appointments(
    skip: int = 0,
    limit: int = 100,
    patient_id: Optional[str] = None,
    doctor_id: Optional[str] = None,
    date: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of appointments"""
    query = db.query(models.Appointment)
    
    if patient_id:
        query = query.filter(models.Appointment.patient_id == patient_id)
    
    if doctor_id:
        query = query.filter(models.Appointment.doctor_id == doctor_id)
    
    if date:
        try:
            filter_date = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(
                db.func.date(models.Appointment.appointment_date) == filter_date
            )
        except:
            pass
    
    if status:
        query = query.filter(models.Appointment.status == status)
    
    appointments = query.offset(skip).limit(limit).all()
    return {
        "count": len(appointments),
        "appointments": [a.to_dict() for a in appointments]
    }

@app.post("/api/appointments")
async def create_appointment(
    patient_id: str,
    doctor_id: str,
    appointment_date: str,
    appointment_time: str,
    type: str = "consultation",
    duration: int = 30,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a new appointment"""
    try:
        # Check if patient exists
        patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Check if doctor exists
        doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        
        # Parse datetime
        appointment_datetime_str = f"{appointment_date} {appointment_time}"
        appointment_datetime = datetime.strptime(appointment_datetime_str, "%Y-%m-%d %H:%M")
        
        # Check if doctor is available at that time
        # (In a real system, you'd check against doctor's schedule)
        
        # Create appointment
        appointment = models.Appointment(
            id=str(uuid.uuid4()),
            appointment_number=generate_appointment_number(),
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_datetime,
            duration=duration,
            status="scheduled",
            type=type,
            notes=notes,
            created_at=datetime.utcnow()
        )
        
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        
        return {
            "message": "Appointment scheduled successfully",
            "appointment_id": appointment.id,
            "appointment_number": appointment.appointment_number,
            "appointment": appointment.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating appointment: {str(e)}")

@app.put("/api/appointments/{appointment_id}/status")
async def update_appointment_status(
    appointment_id: str,
    status: str,
    db: Session = Depends(get_db)
):
    """Update appointment status"""
    valid_statuses = ["scheduled", "confirmed", "cancelled", "completed"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    try:
        appointment.status = status
        db.commit()
        db.refresh(appointment)
        
        return {
            "message": f"Appointment status updated to '{status}'",
            "appointment": appointment.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating appointment: {str(e)}")

# ==================== DASHBOARD ENDPOINTS ====================

@app.get("/api/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    total_patients = db.query(models.Patient).count()
    active_patients = db.query(models.Patient).filter(models.Patient.is_active == True).count()
    total_doctors = db.query(models.Doctor).count()
    available_doctors = db.query(models.Doctor).filter(models.Doctor.is_available == True).count()
    total_appointments = db.query(models.Appointment).count()
    today_appointments = db.query(models.Appointment).filter(
        db.func.date(models.Appointment.appointment_date) == date.today()
    ).count()
    
    # Recent appointments
    recent_appointments = db.query(models.Appointment)\
        .order_by(models.Appointment.appointment_date.desc())\
        .limit(5)\
        .all()
    
    return {
        "stats": {
            "total_patients": total_patients,
            "active_patients": active_patients,
            "total_doctors": total_doctors,
            "available_doctors": available_doctors,
            "total_appointments": total_appointments,
            "today_appointments": today_appointments
        },
        "recent_appointments": [a.to_dict() for a in recent_appointments]
    }

# ==================== SEARCH ENDPOINTS ====================

@app.get("/api/search")
async def search(
    q: str,
    search_type: str = "all",  # all, patients, doctors
    db: Session = Depends(get_db)
):
    """Search across the system"""
    results = {}
    
    if search_type in ["all", "patients"]:
        patients = db.query(models.Patient).filter(
            (models.Patient.first_name.ilike(f"%{q}%")) |
            (models.Patient.last_name.ilike(f"%{q}%")) |
            (models.Patient.mrn.ilike(f"%{q}%")) |
            (models.Patient.contact_number.ilike(f"%{q}%"))
        ).limit(10).all()
        results["patients"] = [p.to_dict() for p in patients]
    
    if search_type in ["all", "doctors"]:
        doctors = db.query(models.Doctor).filter(
            (models.Doctor.first_name.ilike(f"%{q}%")) |
            (models.Doctor.last_name.ilike(f"%{q}%")) |
            (models.Doctor.specialization.ilike(f"%{q}%")) |
            (models.Doctor.license_number.ilike(f"%{q}%"))
        ).limit(10).all()
        results["doctors"] = [d.to_dict() for d in doctors]
    
    return results

# ==================== MEDICAL RECORDS ENDPOINTS ====================

@app.get("/api/patients/{patient_id}/medical-records")
async def get_patient_medical_records(
    patient_id: str,
    db: Session = Depends(get_db)
):
    """Get medical records for a patient"""
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    records = db.query(models.MedicalRecord)\
        .filter(models.MedicalRecord.patient_id == patient_id)\
        .order_by(models.MedicalRecord.visit_date.desc())\
        .all()
    
    return {
        "patient": patient.to_dict(),
        "medical_records": [
            {
                "id": r.id,
                "visit_date": r.visit_date.isoformat() if r.visit_date else None,
                "doctor_id": r.doctor_id,
                "subjective": r.subjective,
                "assessment": r.assessment,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in records
        ]
    }

# Run the app
if __name__ == "__main__":
    print("=" * 60)
    print(" HOSPITAL MANAGEMENT SYSTEM")
    print("=" * 60)
    print("Starting server on http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
