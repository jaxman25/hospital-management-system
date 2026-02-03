from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models import Appointment, Patient, Doctor
from ..schemas import AppointmentCreate, Appointment as AppointmentSchema

router = APIRouter(prefix="/api", tags=["appointments"])

@router.get("/appointments", response_model=List[AppointmentSchema])
def get_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).offset(skip).limit(limit).all()
    return appointments

@router.get("/appointments/{appointment_id}", response_model=AppointmentSchema)
def get_appointment(appointment_id: str, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.post("/appointments", response_model=AppointmentSchema)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    # Check if patient exists
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Check if doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db_appointment = Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
