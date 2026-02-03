import sys
sys.path.append('.')
from backend.database import SessionLocal
from backend.models import Patient, Doctor, Appointment

db = SessionLocal()

print("=== DATABASE CONTENTS ===")

# Patients
patients = db.query(Patient).all()
print(f"\n👥 PATIENTS ({len(patients)}):")
for p in patients:
    print(f"  - {p.first_name} {p.last_name} (MRN: {p.mrn}, ID: {p.id[:8]}...)")

# Doctors
doctors = db.query(Doctor).all()
print(f"\n👨‍⚕️ DOCTORS ({len(doctors)}):")
for d in doctors:
    print(f"  - Dr. {d.name} ({d.specialization}, ID: {d.id[:8]}...)")

# Appointments
appointments = db.query(Appointment).all()
print(f"\n APPOINTMENTS ({len(appointments)}):")
for a in appointments:
    print(f"  - Appointment ID: {a.id[:8]}...")

db.close()

print(f"\n Total: {len(patients)} patients, {len(doctors)} doctors, {len(appointments)} appointments")
