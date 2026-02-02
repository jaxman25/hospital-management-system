from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud.patients
import schemas.doctor_patient
from database import get_db

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=schemas.doctor_patient.Patient)
def create_patient(patient: schemas.doctor_patient.PatientCreate, db: Session = Depends(get_db)):
    return crud.patients.create_patient(db=db, patient=patient)

@router.get("/", response_model=List[schemas.doctor_patient.Patient])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = crud.patients.get_patients(db, skip=skip, limit=limit)
    return patients

@router.get("/{patient_id}", response_model=schemas.doctor_patient.Patient)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = crud.patients.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = crud.patients.delete_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}
