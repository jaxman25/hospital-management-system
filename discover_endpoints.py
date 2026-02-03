import requests
import json

BASE_URL = "http://localhost:8000"

print("=== Discovering API Endpoints ===")

# Get OpenAPI spec
try:
    response = requests.get(f"{BASE_URL}/openapi.json")
    spec = response.json()
    
    print(f"\n Found {len(spec['paths'])} endpoints:")
    for path, methods in spec['paths'].items():
        print(f"  {path}: {', '.join(methods.keys())}")
        
except Exception as e:
    print(f"Error getting OpenAPI spec: {e}")
    
    # Try common endpoints
    print("\n🔍 Trying common endpoints...")
    endpoints = [
        "/",
        "/api/health",
        "/api/patients",
        "/api/doctors", 
        "/api/appointments",
        "/api/users",
        "/api/auth",
        "/dashboard",
        "/doctors",
        "/patients"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=2)
            print(f"  {endpoint}: {response.status_code}")
        except:
            print(f"  {endpoint}:  Not found or error")
