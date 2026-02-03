import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

class HospitalAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
    
    def test_endpoint(self, method, endpoint, data=None, expected_status=200):
        url = f"{BASE_URL}{endpoint}"
        try:
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                response = self.session.post(url, json=data)
            elif method == "PUT":
                response = self.session.put(url, json=data)
            elif method == "DELETE":
                response = self.session.delete(url)
            else:
                return False
            
            success = response.status_code == expected_status
            result = {
                "endpoint": endpoint,
                "method": method,
                "status": response.status_code,
                "success": success,
                "response": response.json() if response.content else None
            }
            self.test_results.append(result)
            return success
            
        except Exception as e:
            result = {
                "endpoint": endpoint,
                "method": method,
                "status": "ERROR",
                "success": False,
                "error": str(e)
            }
            self.test_results.append(result)
            return False
    
    def run_all_tests(self):
        print(" Hospital Management System - API Test Suite")
        print("=" * 50)
        
        # Test basic endpoints
        print("\n1. Basic Endpoints:")
        self.test_endpoint("GET", "/")
        self.test_endpoint("GET", "/api/health")
        self.test_endpoint("GET", "/docs")
        
        # Test data endpoints
        print("\n2. Data Endpoints (GET):")
        self.test_endpoint("GET", "/api/patients")
        self.test_endpoint("GET", "/api/doctors")
        self.test_endpoint("GET", "/api/appointments")
        
        # Try to create data (might fail if POST not implemented)
        print("\n3. Data Creation (POST - might fail):")
        
        # Test patient creation
        test_patient = {
            "mrn": f"TEST{datetime.now().strftime('%H%M%S')}",
            "first_name": "API",
            "last_name": "Test",
            "date_of_birth": "1990-01-01T00:00:00",
            "gender": "Other",
            "contact_number": "555-1234"
        }
        self.test_endpoint("POST", "/api/patients", test_patient, 201)
        
        # Test doctor creation
        test_doctor = {
            "name": "Dr. API Test",
            "specialization": "Testing",
            "contact": "555-5678",
            "email": "test@hospital.com"
        }
        self.test_endpoint("POST", "/api/doctors", test_doctor, 201)
        
        # Print results
        print("\n" + "=" * 50)
        print(" Test Results Summary:")
        print("=" * 50)
        
        for i, result in enumerate(self.test_results, 1):
            status_icon = "" if result["success"] else ""
            print(f"{i}. {status_icon} {result['method']} {result['endpoint']}")
            print(f"   Status: {result['status']}")
            if "error" in result:
                print(f"   Error: {result['error']}")
            print()
        
        # Calculate success rate
        total = len(self.test_results)
        successful = sum(1 for r in self.test_results if r["success"])
        success_rate = (successful / total) * 100 if total > 0 else 0
        
        print(f" Success Rate: {success_rate:.1f}% ({successful}/{total})")
        
        # Recommendations
        print("\n Recommendations:")
        if success_rate < 100:
            print("1. Some endpoints are missing or not working")
            print("2. Check /docs for available endpoints")
            print("3. POST endpoints might need to be implemented")
        else:
            print("1. All tests passed! API is fully functional")
            print("2. Consider adding more features")
        
        return self.test_results

if __name__ == "__main__":
    tester = HospitalAPITester()
    results = tester.run_all_tests()
