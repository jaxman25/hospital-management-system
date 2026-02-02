from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud.doctors
import schemas.doctor_patient
from database import get_db

router = APIRouter(prefix="/doctors", tags=["doctors"])

@router.post("/", response_model=schemas.doctor_patient.Doctor)
def create_doctor(doctor: schemas.doctor_patient.DoctorCreate, db: Session = Depends(get_db)):
    return crud.doctors.create_doctor(db=db, doctor=doctor)

@router.get("/", response_model=List[schemas.doctor_patient.Doctor])
def read_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = crud.doctors.get_doctors(db, skip=skip, limit=limit)
    return doctors

@router.get("/{doctor_id}", response_model=schemas.doctor_patient.Doctor)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = crud.doctors.get_doctor(db, doctor_id=doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor

@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = crud.doctors.delete_doctor(db, doctor_id=doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": "Doctor deleted successfully"}
