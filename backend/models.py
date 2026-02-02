from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from database import Base
import json

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mrn = Column(String(50), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(String(10))
    blood_group = Column(String(5))
    contact_number = Column(String(20))
    email = Column(String(255), unique=True)
    emergency_contact = Column(Text)  # JSON as string
    address = Column(Text)  # JSON as string
    insurance_provider = Column(String(100))
    insurance_number = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="patient")
    medical_records = relationship("MedicalRecord", back_populates="patient")
    prescriptions = relationship("Prescription", back_populates="patient")
    bills = relationship("Bill", back_populates="patient")
    
    def to_dict(self):
        return {
            "id": self.id,
            "mrn": self.mrn,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "gender": self.gender,
            "blood_group": self.blood_group,
            "contact_number": self.contact_number,
            "email": self.email,
            "emergency_contact": json.loads(self.emergency_contact) if self.emergency_contact else {},
            "address": json.loads(self.address) if self.address else {},
            "insurance_provider": self.insurance_provider,
            "insurance_number": self.insurance_number,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_active": self.is_active
        }

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    license_number = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    specialization = Column(String(100))
    department = Column(String(100))
    qualifications = Column(Text)  # JSON as string
    consultation_fee = Column(Float, default=0.0)
    available_days = Column(Text)  # JSON as string
    available_hours = Column(Text)  # JSON as string
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="doctor")
    medical_records = relationship("MedicalRecord", back_populates="doctor")
    prescriptions = relationship("Prescription", back_populates="doctor")
    
    def to_dict(self):
        return {
            "id": self.id,
            "license_number": self.license_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "specialization": self.specialization,
            "department": self.department,
            "qualifications": json.loads(self.qualifications) if self.qualifications else [],
            "consultation_fee": self.consultation_fee,
            "available_days": json.loads(self.available_days) if self.available_days else [],
            "available_hours": json.loads(self.available_hours) if self.available_hours else {},
            "is_available": self.is_available,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    appointment_number = Column(String(50), unique=True, nullable=False)
    patient_id = Column(String(36), ForeignKey("patients.id"))
    doctor_id = Column(String(36), ForeignKey("doctors.id"))
    appointment_date = Column(DateTime, nullable=False)
    duration = Column(Integer, default=30)  # minutes
    status = Column(String(20), default="scheduled")  # scheduled, confirmed, cancelled, completed
    type = Column(String(20))  # consultation, follow-up, surgery
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    
    def to_dict(self):
        return {
            "id": self.id,
            "appointment_number": self.appointment_number,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "appointment_date": self.appointment_date.isoformat() if self.appointment_date else None,
            "duration": self.duration,
            "status": self.status,
            "type": self.type,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "patient_name": f"{self.patient.first_name} {self.patient.last_name}" if self.patient else None,
            "doctor_name": f"Dr. {self.doctor.first_name} {self.doctor.last_name}" if self.doctor else None
        }

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.id"))
    doctor_id = Column(String(36), ForeignKey("doctors.id"))
    visit_date = Column(DateTime, default=datetime.utcnow)
    subjective = Column(Text)  # Patient complaints
    objective = Column(Text)  # Doctor observations
    assessment = Column(Text)  # Diagnosis
    plan = Column(Text)  # Treatment plan
    vital_signs = Column(Text)  # JSON as string
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="medical_records")
    doctor = relationship("Doctor", back_populates="medical_records")

class Prescription(Base):
    __tablename__ = "prescriptions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.id"))
    doctor_id = Column(String(36), ForeignKey("doctors.id"))
    medication_name = Column(String(200), nullable=False)
    dosage = Column(String(100))
    frequency = Column(String(100))
    duration = Column(String(100))
    instructions = Column(Text)
    date_prescribed = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")

class Bill(Base):
    __tablename__ = "bills"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    bill_number = Column(String(50), unique=True, nullable=False)
    patient_id = Column(String(36), ForeignKey("patients.id"))
    amount = Column(Float, nullable=False)
    tax = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    payment_status = Column(String(20), default="pending")  # pending, partial, paid
    payment_method = Column(String(50))
    insurance_claim_id = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    
    # Relationships
    patient = relationship("Patient", back_populates="bills")
