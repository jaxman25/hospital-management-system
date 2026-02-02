import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
import crud.doctors
import crud.patients
from schemas.doctor_patient import DoctorCreate, PatientCreate
from datetime import date

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    print("=== Creating Sample Hospital Data ===")
    
    # Create sample doctors
    doctors = [
        DoctorCreate(
            name="Dr. Sarah Johnson",
            specialization="Pediatrics",
            email="sarah.johnson@hospital.com",
            phone="555-0101"
        ),
        DoctorCreate(
            name="Dr. Michael Chen",
            specialization="Orthopedics",
            email="michael.chen@hospital.com",
            phone="555-0102"
        ),
        DoctorCreate(
            name="Dr. Lisa Rodriguez",
            specialization="Dermatology",
            email="lisa.rodriguez@hospital.com",
            phone="555-0103"
        ),
        DoctorCreate(
            name="Dr. James Wilson",
            specialization="Cardiology",
            email="james.wilson@hospital.com",
            phone="555-0104"
        ),
        DoctorCreate(
            name="Dr. Emily Davis",
            specialization="Neurology",
            email="emily.davis@hospital.com",
            phone="555-0105"
        )
    ]
    
    print("\\nCreating sample doctors...")
    created_doctors = []
    for doctor_data in doctors:
        try:
            doctor = crud.doctors.create_doctor(db, doctor_data)
            created_doctors.append(doctor)
            print(f"   Created: Dr. {doctor.name} - {doctor.specialization}")
        except Exception as e:
            print(f"   Failed to create {doctor_data.name}: {e}")
    
    # Create sample patients
    patients = [
        PatientCreate(
            name="Robert Wilson",
            date_of_birth=date(1985, 3, 22),
            gender="Male",
            email="robert.wilson@example.com",
            phone="555-0201",
            address="123 Main St, Cityville",
            emergency_contact="555-0301",
            blood_type="A+"
        ),
        PatientCreate(
            name="Emily Davis",
            date_of_birth=date(1992, 7, 14),
            gender="Female",
            email="emily.davis@example.com",
            phone="555-0202",
            address="456 Oak Ave, Townsville",
            emergency_contact="555-0302",
            blood_type="O-"
        ),
        PatientCreate(
            name="James Miller",
            date_of_birth=date(1978, 11, 30),
            gender="Male",
            email="james.miller@example.com",
            phone="555-0203",
            address="789 Pine Rd, Villageton",
            emergency_contact="555-0303",
            blood_type="B+"
        ),
        PatientCreate(
            name="Sophia Garcia",
            date_of_birth=date(1995, 4, 18),
            gender="Female",
            email="sophia.garcia@example.com",
            phone="555-0204",
            address="321 Elm St, Hamletville",
            emergency_contact="555-0304",
            blood_type="AB+"
        ),
        PatientCreate(
            name="David Kim",
            date_of_birth=date(1988, 9, 5),
            gender="Male",
            email="david.kim@example.com",
            phone="555-0205",
            address="654 Maple Dr, Boroughburg",
            emergency_contact="555-0305",
            blood_type="O+"
        )
    ]
    
    print("\\nCreating sample patients...")
    created_patients = []
    for patient_data in patients:
        try:
            patient = crud.patients.create_patient(db, patient_data)
            created_patients.append(patient)
            age = (date.today() - patient.date_of_birth).days // 365
            print(f"   Created: {patient.name}, {age}y, {patient.blood_type}")
        except Exception as e:
            print(f"   Failed to create {patient_data.name}: {e}")
    
    print(f"\\n=== Summary ===")
    print(f"Total Doctors: {len(created_doctors)}")
    print(f"Total Patients: {len(created_patients)}")
    print(f"\\n Sample data creation complete!")
    
except Exception as e:
    print(f"\\n Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
    print("\\nDatabase connection closed.")
