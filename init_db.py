# Database initialization script
from models import db, Patient, Doctor, Appointment
from app import create_app

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created successfully!")
    
    # Create sample data if tables are empty
    if Patient.query.count() == 0:
        print("Creating sample data...")
        
        # Add sample patients
        patients = [
            Patient(name="John Doe", age=45, gender="Male", contact="123-456-7890"),
            Patient(name="Jane Smith", age=32, gender="Female", contact="123-456-7891"),
        ]
        
        for patient in patients:
            db.session.add(patient)
        
        db.session.commit()
        print(f"Added {len(patients)} sample patients")
