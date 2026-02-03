from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import get_db
from backend.models import Doctor
from schemas.doctor_patient import Doctor as DoctorSchema, DoctorCreate

router = APIRouter(prefix="/api", tags=["doctors"])

@router.get("/doctors", response_model=List[DoctorSchema])
def get_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = db.query(Doctor).offset(skip).limit(limit).all()
    return doctors

@router.get("/doctors/{doctor_id}", response_model=DoctorSchema)
def get_doctor(doctor_id: str, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.post("/doctors", response_model=DoctorSchema)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

# Web interface route
@router.get("/doctors/", response_class=HTMLResponse)
async def doctors_page(request: Request):
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse(
        "doctors.html" if os.path.exists("templates/doctors.html") else "base.html",
        {"request": request, "title": "Doctors Management"}
    )
