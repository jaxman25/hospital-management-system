import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("=== Testing Hospital Management System API ===\n")
    
    # 1. Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"   ✅ Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"   ❌ Health failed: {e}")
        return
    
    # 2. Get existing patients
    print("\n2. Getting existing patients...")
    try:
        response = requests.get(f"{BASE_URL}/api/patients")
        patients = response.json()
        print(f"    Found {len(patients)} patients")
    except Exception as e:
        print(f"     Patients endpoint: {e}")
    
    # 3. Get existing doctors
    print("\n3. Getting existing doctors...")
    try:
        response = requests.get(f"{BASE_URL}/api/doctors")
        doctors = response.json()
        print(f"    Found {len(doctors)} doctors")
    except Exception as e:
        print(f"     Doctors endpoint: {e}")
    
    # 4. Create a test patient (if API allows)
    print("\n4. Testing patient creation...")
    test_patient = {
        "mrn": "TEST001",
        "first_name": "Test",
        "last_name": "Patient",
        "date_of_birth": "1990-01-01T00:00:00",
        "gender": "Male",
        "contact_number": "123-456-7890"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/patients", json=test_patient)
        if response.status_code in [200, 201]:
            print(f"    Created test patient: {response.json()['first_name']} {response.json()['last_name']}")
        else:
            print(f"     Patient creation returned: {response.status_code}")
    except Exception as e:
        print(f"     Patient creation failed (might need schema adjustment): {e}")
    
    print("\n=== API Test Complete ===")
    print(f"\n Dashboard: {BASE_URL}")
    print(f" API Docs: {BASE_URL}/docs")
    print(f" Health: {BASE_URL}/api/health")

if __name__ == "__main__":
    test_api()
