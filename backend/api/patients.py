from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Patient
from ..schemas import PatientCreate, Patient as PatientSchema

router = APIRouter(prefix="/api", tags=["patients"])

@router.get("/patients", response_model=List[PatientSchema])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return patients

@router.get("/patients/{patient_id}", response_model=PatientSchema)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/patients", response_model=PatientSchema)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    # In a real app, you'd generate MRN, validate data, etc.
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient
