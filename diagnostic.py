import sys
import os

print("=== Hospital System Diagnostic ===")

# Check Python path
print(f"\n1. Python Path:")
for path in sys.path:
    print(f"   {path}")

# Check if modules exist
print(f"\n2. Module Availability:")
modules = ["routes.dashboard", "routes.doctors", "routes.patients", "backend.database", "backend.models"]
for module in modules:
    try:
        __import__(module)
        print(f"    {module}")
    except ImportError as e:
        print(f"    {module}: {e}")

# Check file existence
print(f"\n3. File Existence:")
files = [
    "routes/__init__.py",
    "routes/dashboard.py", 
    "routes/doctors.py",
    "routes/patients.py",
    "backend/database.py",
    "backend/models.py",
    "schemas/doctor_patient.py",
    "main.py"
]

for file in files:
    exists = os.path.exists(file)
    status = "" if exists else ""
    print(f"   {status} {file}")

print(f"\n=== Diagnostic Complete ===")
