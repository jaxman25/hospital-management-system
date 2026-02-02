from sqlalchemy.orm import Session
from models.doctor import Doctor as DoctorModel
from schemas.doctor_patient import DoctorCreate

def get_doctor(db: Session, doctor_id: int):
    return db.query(DoctorModel).filter(DoctorModel.id == doctor_id).first()

def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DoctorModel).offset(skip).limit(limit).all()

def create_doctor(db: Session, doctor: DoctorCreate):
    from datetime import date
    db_doctor = DoctorModel(
        name=doctor.name,
        specialization=doctor.specialization,
        email=doctor.email,
        phone=doctor.phone,
        created_at=date.today()
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def delete_doctor(db: Session, doctor_id: int):
    doctor = db.query(DoctorModel).filter(DoctorModel.id == doctor_id).first()
    if doctor:
        db.delete(doctor)
        db.commit()
    return doctor
