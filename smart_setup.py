"""
Smart demo data setup - automatically adapts to model structure
"""

from database import SessionLocal, Base, engine
from sqlalchemy.orm import Session
import inspect

def get_model_fields(model_class):
    """Get all column names from a SQLAlchemy model"""
    return [column.name for column in model_class.__table__.columns]

def create_smart_sample(db: Session):
    """Create sample data based on actual model fields"""
    
    # Import models
    from models.doctor import Doctor
    from models.patient import Patient
    from models.appointment import Appointment
    
    print("\n Detecting model structures...")
    
    # Doctor fields
    doctor_fields = get_model_fields(Doctor)
    print(f" Doctor fields: {doctor_fields}")
    
    # Patient fields  
    patient_fields = get_model_fields(Patient)
    print(f" Patient fields: {patient_fields}")
    
    # Appointment fields
    appointment_fields = get_model_fields(Appointment)
    print(f" Appointment fields: {appointment_fields}")
    
    print("\n Creating sample data...")
    
    # Create doctors - only use fields that exist
    doctors_data = [
        {"name": "Dr. Sarah Johnson", "specialization": "Cardiology", "email": "sarah@hospital.com"},
        {"name": "Dr. Michael Chen", "specialization": "Neurology", "email": "michael@hospital.com"},
        {"name": "Dr. Emily Wilson", "specialization": "Pediatrics", "email": "emily@hospital.com"},
        {"name": "Dr. James Rodriguez", "specialization": "Orthopedics", "email": "james@hospital.com"}
    ]
    
    doctors = []
    for data in doctors_data:
        # Filter to only include fields that exist in the model
        filtered_data = {k: v for k, v in data.items() if k in doctor_fields}
        doctors.append(Doctor(**filtered_data))
    
    for doctor in doctors:
        db.add(doctor)
    db.commit()
    print(f" Created {len(doctors)} doctors")
    
    # Create patients - adapt based on available fields
    patients_data = []
    
    # Try different field combinations based on what might exist
    sample_patients = [
        {"name": "John Smith"},
        {"name": "Maria Garcia"},
        {"name": "Robert Johnson"},
        {"name": "Lisa Wang"},
        {"name": "David Brown"}
    ]
    
    # Add additional fields if they exist in the model
    extra_fields = {
        "age": [45, 32, 58, 28, 65],
        "gender": ["Male", "Female", "Male", "Female", "Male"],
        "email": ["john@email.com", "maria@email.com", "robert@email.com", "lisa@email.com", "david@email.com"],
        "phone": ["555-0101", "555-0102", "555-0103", "555-0104", "555-0105"],
        "address": ["123 Main St", "456 Oak Ave", "789 Pine Rd", "321 Elm St", "654 Maple Dr"],
        "date_of_birth": ["1978-05-15", "1991-08-22", "1965-03-10", "1995-11-30", "1958-07-04"]
    }
    
    for i, patient in enumerate(sample_patients):
        # Add extra fields that exist in the model
        for field, values in extra_fields.items():
            if field in patient_fields and i < len(values):
                patient[field] = values[i]
        
        patients_data.append(patient)
    
    patients = []
    for data in patients_data:
        # Filter to only include fields that exist in the model
        filtered_data = {k: v for k, v in data.items() if k in patient_fields}
        patients.append(Patient(**filtered_data))
    
    for patient in patients:
        db.add(patient)
    db.commit()
    print(f" Created {len(patients)} patients")
    
    # Create appointments if we have both patients and doctors
    if patients and doctors and hasattr(Appointment, 'patient_id') and hasattr(Appointment, 'doctor_id'):
        appointments = [
            {"patient_id": patients[0].id, "doctor_id": doctors[0].id, "reason": "Routine checkup"},
            {"patient_id": patients[1].id, "doctor_id": doctors[1].id, "reason": "Headache consultation"},
            {"patient_id": patients[2].id, "doctor_id": doctors[2].id, "reason": "Child vaccination"},
            {"patient_id": patients[3].id, "doctor_id": doctors[3].id, "reason": "Knee pain evaluation"}
        ]
        
        # Add appointment_date if field exists
        if 'appointment_date' in appointment_fields:
            dates = ["2024-02-10", "2024-02-10", "2024-02-11", "2024-02-12"]
            for i, appt in enumerate(appointments):
                appt['appointment_date'] = dates[i]
        
        # Add status if field exists
        if 'status' in appointment_fields:
            statuses = ["Scheduled", "Completed", "Scheduled", "Pending"]
            for i, appt in enumerate(appointments):
                appt['status'] = statuses[i]
        
        appointment_objs = []
        for data in appointments:
            # Filter to only include fields that exist in the model
            filtered_data = {k: v for k, v in data.items() if k in appointment_fields}
            appointment_objs.append(Appointment(**filtered_data))
        
        for appointment in appointment_objs:
            db.add(appointment)
        db.commit()
        print(f" Created {len(appointment_objs)} appointments")
    else:
        print("  Skipping appointments (missing required fields)")
    
    return True

def main():
    print("\n" + "="*60)
    print(" SMART DEMO DATA SETUP FOR PRESENTATION")
    print("="*60)
    
    # Clear and create tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print(" Database initialized")
    
    db = SessionLocal()
    try:
        success = create_smart_sample(db)
        
        if success:
            print("\n" + "="*60)
            print(" DEMO DATA SETUP COMPLETE!")
            print("="*60)
            print("\n Your system now contains:")
            print("     Sample Doctors")
            print("     Sample Patients") 
            print("     Sample Appointments (if supported)")
            print("\n Ready for professional presentation!")
            print("   Start server: python main.py")
            print("   Access at: http://localhost:8000/")
            print("="*60)
        
    except Exception as e:
        print(f"\n Error during setup: {e}")
        print("\n  Creating minimal database structure...")
        print(" You can add data through the web interface.")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
