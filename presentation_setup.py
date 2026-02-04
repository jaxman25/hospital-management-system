"""
Sample data for presentation to teacher
Run this before presentation to populate the database with demo data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from sqlalchemy.orm import Session

# Clear existing data and create tables
def setup_database():
    from database import Base
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print(" Database tables created")

def create_sample_data(db: Session):
    # First, check what fields Doctor model has
    print("\n Checking Doctor model fields...")
    doctor_columns = [column.name for column in Doctor.__table__.columns]
    print(f"Doctor model has fields: {doctor_columns}")
    
    # Create sample doctors - adjust based on actual model
    doctors_data = [
        {
            "name": "Dr. Sarah Johnson",
            "email": "sarah.johnson@medicare.com",
            "phone": "+1-555-0101",
            "specialization": "Cardiology"  # Changed from specialty to specialization
        },
        {
            "name": "Dr. Michael Chen",
            "email": "michael.chen@medicare.com",
            "phone": "+1-555-0102",
            "specialization": "Neurology"
        },
        {
            "name": "Dr. Emily Wilson",
            "email": "emily.wilson@medicare.com", 
            "phone": "+1-555-0103",
            "specialization": "Pediatrics"
        },
        {
            "name": "Dr. James Rodriguez",
            "email": "james.rodriguez@medicare.com",
            "phone": "+1-555-0104",
            "specialization": "Orthopedics"
        }
    ]
    
    # Filter out fields that don't exist in the model
    valid_doctor_fields = set(doctor_columns)
    doctors = []
    
    for doc_data in doctors_data:
        # Only include fields that exist in the model
        filtered_data = {k: v for k, v in doc_data.items() if k in valid_doctor_fields}
        doctors.append(Doctor(**filtered_data))
    
    for doctor in doctors:
        db.add(doctor)
    db.commit()
    print(f" Created {len(doctors)} sample doctors")
    
    # Create sample patients
    patients = [
        Patient(
            name="John Smith",
            age=45,
            gender="Male",
            address="123 Main St, City",
            phone="+1-555-0201",
            email="john.smith@email.com"
        ),
        Patient(
            name="Maria Garcia",
            age=32,
            gender="Female", 
            address="456 Oak Ave, City",
            phone="+1-555-0202",
            email="maria.garcia@email.com"
        ),
        Patient(
            name="Robert Johnson",
            age=58,
            gender="Male",
            address="789 Pine Rd, City",
            phone="+1-555-0203",
            email="robert.johnson@email.com"
        ),
        Patient(
            name="Lisa Wang",
            age=28,
            gender="Female",
            address="321 Elm St, City",
            phone="+1-555-0204",
            email="lisa.wang@email.com"
        ),
        Patient(
            name="David Brown",
            age=65,
            gender="Male",
            address="654 Maple Dr, City",
            phone="+1-555-0205",
            email="david.brown@email.com"
        )
    ]
    
    for patient in patients:
        db.add(patient)
    db.commit()
    print(f" Created {len(patients)} sample patients")
    
    # Create sample appointments
    appointments = [
        Appointment(
            patient_id=1,
            doctor_id=1,
            appointment_date="2024-02-10",
            appointment_time="09:00",
            reason="Routine checkup",
            status="Scheduled"
        ),
        Appointment(
            patient_id=2,
            doctor_id=2,
            appointment_date="2024-02-10",
            appointment_time="10:30",
            reason="Headache consultation",
            status="Completed"
        ),
        Appointment(
            patient_id=3,
            doctor_id=3,
            appointment_date="2024-02-11",
            appointment_time="14:00",
            reason="Child vaccination",
            status="Scheduled"
        ),
        Appointment(
            patient_id=4,
            doctor_id=4,
            appointment_date="2024-02-12",
            appointment_time="11:00",
            reason="Knee pain evaluation",
            status="Pending"
        )
    ]
    
    for appointment in appointments:
        db.add(appointment)
    db.commit()
    print(f" Created {len(appointments)} sample appointments")

def main():
    print("\n" + "="*60)
    print(" SETTING UP DEMO DATA FOR PRESENTATION")
    print("="*60)
    
    setup_database()
    
    db = SessionLocal()
    try:
        create_sample_data(db)
        print("\n Demo data setup complete!")
        print("\n Sample Data Created:")
        print("    4 Doctors")
        print("    5 Patients")
        print("    4 Appointments")
        print("\n Ready for presentation!")
        print("   Access at: http://localhost:8000/")
    except Exception as e:
        print(f"\n Error: {e}")
        print("\n  Trying alternative approach...")
        # Try simpler approach
        db.rollback()
        create_simple_data(db)
    finally:
        db.close()

def create_simple_data(db: Session):
    """Alternative simpler data creation"""
    print("\n Creating simple sample data...")
    
    # Create minimal doctors
    doctor1 = Doctor(name="Dr. Sarah Johnson", email="sarah@hospital.com")
    doctor2 = Doctor(name="Dr. Michael Chen", email="michael@hospital.com")
    db.add_all([doctor1, doctor2])
    db.commit()
    
    # Create minimal patients
    patient1 = Patient(name="John Smith", age=45, gender="Male")
    patient2 = Patient(name="Maria Garcia", age=32, gender="Female")
    db.add_all([patient1, patient2])
    db.commit()
    
    # Create appointment
    appointment = Appointment(
        patient_id=1,
        doctor_id=1,
        appointment_date="2024-02-10",
        reason="Checkup"
    )
    db.add(appointment)
    db.commit()
    
    print(" Simple sample data created!")

if __name__ == "__main__":
    main()
