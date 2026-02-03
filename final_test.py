import requests
import time

BASE_URL = "http://localhost:8000"

def wait_for_server(max_retries=10, delay=2):
    """Wait for server to be ready"""
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except:
            print(f"  Waiting for server... ({i+1}/{max_retries})")
            time.sleep(delay)
    return False

def run_tests():
    print("🏥 Hospital Management System - Final Test")
    print("=" * 50)
    
    # Wait for server
    if not wait_for_server():
        print(" Server did not start in time")
        return
    
    # Test endpoints
    endpoints = [
        ("/", "Root"),
        ("/api/health", "Health Check"),
        ("/api/doctors", "Doctors API"),
        ("/api/patients", "Patients API"),
        ("/dashboard", "Dashboard"),
        ("/docs", "API Documentation"),
    ]
    
    results = []
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            status = "" if response.status_code == 200 else ""
            results.append((name, status, response.status_code))
        except Exception as e:
            results.append((name, "", str(e)))
    
    # Print results
    print("\n Test Results:")
    print("-" * 50)
    for name, status, detail in results:
        print(f"{status} {name}: {detail}")
    
    # Summary
    success = sum(1 for _, status, _ in results if status == "")
    total = len(results)
    
    print(f"\n Success Rate: {success}/{total} ({success/total*100:.0f}%)")
    
    if success == total:
        print("\n CONGRATULATIONS! All tests passed!")
        print("\nYour Hospital Management System is fully operational!")
        print(f"\n Dashboard: {BASE_URL}/dashboard")
        print(f" API Docs: {BASE_URL}/docs")
        print(f" Doctors: {BASE_URL}/api/doctors")
        print(f" Patients: {BASE_URL}/api/patients")
    else:
        print("\n  Some tests failed. Check the server output for errors.")

if __name__ == "__main__":
    run_tests()
