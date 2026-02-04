from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from models.patient import Patient

# Try to import from schemas.doctor_patient (based on your original file)
try:
    from schemas.doctor_patient import Patient as PatientSchema, PatientCreate, PatientUpdate
    print("Using schemas.doctor_patient for patients")
except ImportError:
    # If that fails, create simple schemas
    from pydantic import BaseModel
    from typing import Optional
    from datetime import date
    
    class PatientCreate(BaseModel):
        name: str
        age: int
        gender: str
        address: Optional[str] = None
        phone: Optional[str] = None
        email: Optional[str] = None
        
    class PatientUpdate(BaseModel):
        name: Optional[str] = None
        age: Optional[int] = None
        gender: Optional[str] = None
        address: Optional[str] = None
        phone: Optional[str] = None
        email: Optional[str] = None
        
    class PatientSchema(BaseModel):
        id: int
        name: str
        age: int
        gender: str
        address: Optional[str] = None
        phone: Optional[str] = None
        email: Optional[str] = None
        
        class Config:
            from_attributes = True

router = APIRouter()

# HTML Routes
@router.get("/patients/", response_class=HTMLResponse)
async def list_patients_html(request: Request, db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return {'request': request, 'patients': patients}

@router.get("/patients/{patient_id}", response_class=HTMLResponse)
async def get_patient_html(patient_id: int, request: Request, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {'request': request, 'patient': patient}

# API Routes
@router.get("/api/patients")
async def list_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return patients

@router.get("/api/patients/{patient_id}")
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/api/patients")
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.put("/api/patients/{patient_id}")
async def update_patient(patient_id: int, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    for key, value in patient_update.dict(exclude_unset=True).items():
        setattr(db_patient, key, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.delete("/api/patients/{patient_id}")
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}
