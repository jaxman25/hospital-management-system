from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import get_db
from backend.models import Patient
from schemas.doctor_patient import Patient as PatientSchema, PatientCreate

router = APIRouter(prefix="/api", tags=["patients"])

@router.get("/patients", response_model=List[PatientSchema])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return patients

@router.get("/patients/{patient_id}", response_model=PatientSchema)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/patients", response_model=PatientSchema)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# Web interface route
@router.get("/patients/", response_class=HTMLResponse)
async def patients_page(request: Request):
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse(
        "patients.html" if os.path.exists("templates/patients.html") else "base.html",
        {"request": request, "title": "Patients Management"}
    )
