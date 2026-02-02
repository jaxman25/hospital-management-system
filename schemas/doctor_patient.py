from pydantic import BaseModel
from datetime import date
from typing import Optional

class DoctorBase(BaseModel):
    name: str
    specialization: str
    email: str
    phone: Optional[str] = None

class DoctorCreate(DoctorBase):
    pass

class Doctor(DoctorBase):
    id: int
    created_at: date
    
    class Config:
        from_attributes = True

class PatientBase(BaseModel):
    name: str
    date_of_birth: date
    gender: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    emergency_contact: Optional[str] = None
    blood_type: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    created_at: date
    
    class Config:
        from_attributes = True
