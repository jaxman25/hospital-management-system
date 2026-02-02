from sqlalchemy.orm import Session
from models.patient import Patient as PatientModel
from schemas.doctor_patient import PatientCreate

def get_patient(db: Session, patient_id: int):
    return db.query(PatientModel).filter(PatientModel.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PatientModel).offset(skip).limit(limit).all()

def create_patient(db: Session, patient: PatientCreate):
    from datetime import date
    db_patient = PatientModel(
        name=patient.name,
        date_of_birth=patient.date_of_birth,
        gender=patient.gender,
        address=patient.address,
        phone=patient.phone,
        email=patient.email,
        emergency_contact=patient.emergency_contact,
        blood_type=patient.blood_type,
        created_at=date.today()
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if patient:
        db.delete(patient)
        db.commit()
    return patient
