# Hospital Management System API Testing Script
# Usage: .\hospital_api.ps1

Write-Host "=== Hospital Management System API Tests ===" -ForegroundColor Cyan
Write-Host "Starting at: 02/02/2026 15:42:30" -ForegroundColor Gray
Write-Host ""

# Test 1: Health Check
Write-Host "1. Testing Health Check..." -ForegroundColor Yellow
try {
    \ = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -Method Get -ErrorAction Stop
    Write-Host "    Health Status: \" -ForegroundColor Green
    Write-Host "    Service: \" -ForegroundColor Green
    Write-Host "    Database: \" -ForegroundColor Green
} catch {
    Write-Host "    Health check failed: \" -ForegroundColor Red
    exit 1
}

# Test 2: System Info
Write-Host "\
2. Testing System Info..." -ForegroundColor Yellow
try {
    \ = Invoke-RestMethod -Uri "http://localhost:8000/api/info" -Method Get -ErrorAction Stop
    if (\ -and \.python_version) {
        Write-Host "    Python: \" -ForegroundColor Green
        Write-Host "    FastAPI: \" -ForegroundColor Green
        Write-Host "    System: \" -ForegroundColor Green
    } else {
        Write-Host "    System info returned unexpected format" -ForegroundColor Yellow
    }
} catch {
    Write-Host "    System info failed: \" -ForegroundColor Red
}

# Test 3: Dashboard Access
Write-Host "\
3. Testing Dashboard..." -ForegroundColor Yellow
try {
    \ = Invoke-WebRequest -Uri "http://localhost:8000/dashboard" -Method Get -ErrorAction Stop
    Write-Host "    Dashboard is accessible (Status: \)" -ForegroundColor Green
} catch {
    Write-Host "    Dashboard is not accessible: \" -ForegroundColor Red
}

# Test 4: API Documentation
Write-Host "\
4. Testing API Documentation..." -ForegroundColor Yellow
try {
    \ = Invoke-WebRequest -Uri "http://localhost:8000/docs" -Method Get -ErrorAction Stop
    Write-Host "    API Documentation is accessible (Status: \)" -ForegroundColor Green
} catch {
    Write-Host "    API Documentation is not accessible: \" -ForegroundColor Red
}

# Test 5: List Doctors (existing data)
Write-Host "\
5. Listing Existing Doctors..." -ForegroundColor Yellow
try {
    \ = Invoke-RestMethod -Uri "http://localhost:8000/doctors/" -Method Get -ErrorAction Stop
    Write-Host "    Found \ doctors in database" -ForegroundColor Green
    if (\.Count -gt 0) {
        foreach (\ in \) {
            Write-Host "     - \ (\)" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "    Failed to list doctors: \" -ForegroundColor Red
}

# Test 6: List Patients (existing data)
Write-Host "\
6. Listing Existing Patients..." -ForegroundColor Yellow
try {
    \ = Invoke-RestMethod -Uri "http://localhost:8000/patients/" -Method Get -ErrorAction Stop
    Write-Host "    Found \ patients in database" -ForegroundColor Green
    if (\.Count -gt 0) {
        foreach (\ in \) {
            \ = [math]::Floor(((Get-Date) - (Get-Date \.date_of_birth)).TotalDays / 365.25)
            Write-Host "     - \, \ y/o, \" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "    Failed to list patients: \" -ForegroundColor Red
}

# Test 7: Create a new doctor
Write-Host "\
7. Creating a New Doctor..." -ForegroundColor Yellow
try {
    \ = @{
        name = "Dr. Test Physician"
        specialization = "General Medicine"
        email = "test.doctor@hospital.com"
        phone = "555-9999"
    } | ConvertTo-Json
    
    \ = Invoke-RestMethod -Uri "http://localhost:8000/doctors/" -Method Post -Body \ -ContentType "application/json" -ErrorAction Stop
    Write-Host "    Created new doctor: \" -ForegroundColor Green
    Write-Host "     ID: \, Email: \" -ForegroundColor Gray
} catch {
    Write-Host "    Failed to create new doctor: \" -ForegroundColor Red
}

# Test 8: Create a new patient
Write-Host "\
8. Creating a New Patient..." -ForegroundColor Yellow
try {
    \ = @{
        name = "Test Patient"
        date_of_birth = "2000-01-01"
        gender = "Other"
        email = "test.patient@example.com"
        phone = "555-8888"
        blood_type = "A+"
    } | ConvertTo-Json
    
    \ = Invoke-RestMethod -Uri "http://localhost:8000/patients/" -Method Post -Body \ -ContentType "application/json" -ErrorAction Stop
    Write-Host "    Created new patient: \" -ForegroundColor Green
    Write-Host "     ID: \, DOB: \" -ForegroundColor Gray
} catch {
    Write-Host "    Failed to create new patient: \" -ForegroundColor Red
}

# Test 9: Updated counts
Write-Host "\
9. Checking Updated Counts..." -ForegroundColor Yellow
try {
    \ = Invoke-RestMethod -Uri "http://localhost:8000/doctors/" -Method Get -ErrorAction Stop
    \ = Invoke-RestMethod -Uri "http://localhost:8000/patients/" -Method Get -ErrorAction Stop
    Write-Host "    Total Doctors: \" -ForegroundColor Green
    Write-Host "    Total Patients: \" -ForegroundColor Green
} catch {
    Write-Host "    Failed to get updated counts: \" -ForegroundColor Red
}

# Test 10: Delete test data
Write-Host "\
10. Cleaning Up Test Data..." -ForegroundColor Yellow
try {
    # List doctors to find test doctor
    \ = Invoke-RestMethod -Uri "http://localhost:8000/doctors/" -Method Get -ErrorAction Stop
    \ = \ | Where-Object { \.email -eq "test.doctor@hospital.com" } | Select-Object -First 1
    if (\) {
        Invoke-RestMethod -Uri "http://localhost:8000/doctors/\" -Method Delete -ErrorAction Stop | Out-Null
        Write-Host "    Deleted test doctor" -ForegroundColor Green
    }
    
    # List patients to find test patient
    \ = Invoke-RestMethod -Uri "http://localhost:8000/patients/" -Method Get -ErrorAction Stop
    \ = \ | Where-Object { \.email -eq "test.patient@example.com" } | Select-Object -First 1
    if (\) {
        Invoke-RestMethod -Uri "http://localhost:8000/patients/\" -Method Delete -ErrorAction Stop | Out-Null
        Write-Host "    Deleted test patient" -ForegroundColor Green
    }
} catch {
    Write-Host "    Cleanup may have failed: \" -ForegroundColor Yellow
}

# Summary
Write-Host "\
=== Test Summary ===" -ForegroundColor Cyan
Write-Host "Tests Completed: 10" -ForegroundColor Gray
Write-Host "Completed at: \02/02/2026 15:42:30" -ForegroundColor Gray

Write-Host "\
=== Access Your System ===" -ForegroundColor Green
Write-Host "Dashboard: http://localhost:8000/dashboard" -ForegroundColor Yellow
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "Doctors API: http://localhost:8000/doctors/" -ForegroundColor Yellow
Write-Host "Patients API: http://localhost:8000/patients/" -ForegroundColor Yellow
Write-Host "Health Check: http://localhost:8000/api/health" -ForegroundColor Yellow

Write-Host "\
 All tests completed!" -ForegroundColor Green
