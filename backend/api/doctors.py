from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Doctor
from ..schemas import DoctorCreate, Doctor as DoctorSchema

router = APIRouter(prefix="/api", tags=["doctors"])

@router.get("/doctors", response_model=List[DoctorSchema])
def get_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = db.query(Doctor).offset(skip).limit(limit).all()
    return doctors

@router.get("/doctors/{doctor_id}", response_model=DoctorSchema)
def get_doctor(doctor_id: str, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.post("/doctors", response_model=DoctorSchema)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor
