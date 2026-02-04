from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from models.doctor import Doctor

# Try to import from schemas.doctor_patient (based on your original file)
try:
    from schemas.doctor_patient import Doctor as DoctorSchema, DoctorCreate, DoctorUpdate
    print("Using schemas.doctor_patient")
except ImportError:
    # If that fails, create simple schemas
    from pydantic import BaseModel
    from typing import Optional
    
    class DoctorCreate(BaseModel):
        name: str
        specialty: str
        email: Optional[str] = None
        phone: Optional[str] = None
        
    class DoctorUpdate(BaseModel):
        name: Optional[str] = None
        specialty: Optional[str] = None
        email: Optional[str] = None
        phone: Optional[str] = None
        
    class DoctorSchema(BaseModel):
        id: int
        name: str
        specialty: str
        email: Optional[str] = None
        phone: Optional[str] = None
        
        class Config:
            from_attributes = True

router = APIRouter()

# HTML Routes
@router.get("/doctors/", response_class=HTMLResponse)
async def list_doctors_html(request: Request, db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()
    return {'request': request, 'doctors': doctors}

@router.get("/doctors/{doctor_id}", response_class=HTMLResponse)
async def get_doctor_html(doctor_id: int, request: Request, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {'request': request, 'doctor': doctor}

# API Routes
@router.get("/api/doctors")
async def list_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()
    return doctors

@router.get("/api/doctors/{doctor_id}")
async def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.post("/api/doctors")
async def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.put("/api/doctors/{doctor_id}")
async def update_doctor(doctor_id: int, doctor_update: DoctorUpdate, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    for key, value in doctor_update.dict(exclude_unset=True).items():
        setattr(db_doctor, key, value)
    
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.delete("/api/doctors/{doctor_id}")
async def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor deleted successfully"}
