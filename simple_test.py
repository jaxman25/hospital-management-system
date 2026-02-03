import requests
import json

BASE_URL = "http://localhost:8000"

print("=== Testing Fixed Hospital API ===\n")

# Test endpoints
endpoints = [
    ("GET", "/", "Dashboard"),
    ("GET", "/api/health", "Health Check"),
    ("GET", "/api/patients", "Get Patients"),
    ("GET", "/api/doctors", "Get Doctors"),
    ("GET", "/api/appointments", "Get Appointments"),
]

for method, endpoint, name in endpoints:
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
            print(f"{name}: {response.status_code}")
            if response.status_code == 200 and endpoint != "/":
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"  Found {len(data)} items")
                    else:
                        print(f"  Response: {json.dumps(data, indent=2)[:100]}...")
                except:
                    print(f"  HTML response (length: {len(response.text)})")
        print()
    except Exception as e:
        print(f"{name}: ERROR - {e}\n")

print(" Test complete! Open http://localhost:8000/docs for full API documentation")
