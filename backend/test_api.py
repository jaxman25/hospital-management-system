import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    print("Testing Hospital Management System API...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ Root endpoint: {response.status_code} - {response.json()}")
    except:
        print("✗ Cannot connect to server")
        return
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f" Health check: {response.status_code} - {response.json()}")
    except:
        print(" Health endpoint not available")
    
    # Test patients endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/patients")
        print(f" Patients endpoint: {response.status_code}")
    except:
        print(" Patients endpoint not available")
    
    # Test doctors endpoint  
    try:
        response = requests.get(f"{BASE_URL}/api/doctors")
        print(f" Doctors endpoint: {response.status_code}")
    except:
        print(" Doctors endpoint not available")

if __name__ == "__main__":
    test_endpoints()
