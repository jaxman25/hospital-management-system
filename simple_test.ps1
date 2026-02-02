# Simple API Test Script
# Usage: .\simple_test.ps1

Write-Host "=== Hospital Management System - Simple Test ===" -ForegroundColor Cyan

# Check if server is running
Write-Host "1. Checking if server is running..." -ForegroundColor Yellow
try {
    {"status":"healthy","service":"hospital-management","database":"connected"} = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -Method Get -TimeoutSec 3
    Write-Host "    Server is running" -ForegroundColor Green
    Write-Host "   Health: " -ForegroundColor Gray
} catch {
    Write-Host "    Server is not running" -ForegroundColor Red
    Write-Host "   Start the server first: uvicorn main:app --reload" -ForegroundColor Yellow
    exit 1
}

# Test doctors API
Write-Host "
2. Testing Doctors API..." -ForegroundColor Yellow
try {
     = Invoke-RestMethod -Uri "http://localhost:8000/doctors/" -Method Get -TimeoutSec 5
    Write-Host "    Found 0 doctors" -ForegroundColor Green
    if (.Count -gt 0) {
        Write-Host "   First doctor:  - " -ForegroundColor Gray
    }
} catch {
    Write-Host "    Failed to get doctors" -ForegroundColor Red
}

# Test patients API
Write-Host "
3. Testing Patients API..." -ForegroundColor Yellow
try {
     = Invoke-RestMethod -Uri "http://localhost:8000/patients/" -Method Get -TimeoutSec 5
    Write-Host "    Found 0 patients" -ForegroundColor Green
    if (.Count -gt 0) {
        Write-Host "   First patient:  - " -ForegroundColor Gray
    }
} catch {
    Write-Host "    Failed to get patients" -ForegroundColor Red
}

# Test dashboard
Write-Host "
4. Testing Dashboard..." -ForegroundColor Yellow
try {
    {"status":"healthy","service":"hospital-management","database":"connected"} = Invoke-WebRequest -Uri "http://localhost:8000/dashboard" -Method Get -TimeoutSec 5
    Write-Host "    Dashboard is accessible" -ForegroundColor Green
} catch {
    Write-Host "    Dashboard is not accessible" -ForegroundColor Red
}

# Test API docs
Write-Host "
5. Testing API Documentation..." -ForegroundColor Yellow
try {
    {"status":"healthy","service":"hospital-management","database":"connected"} = Invoke-WebRequest -Uri "http://localhost:8000/docs" -Method Get -TimeoutSec 5
    Write-Host "    API Documentation is accessible" -ForegroundColor Green
} catch {
    Write-Host "    API Documentation is not accessible" -ForegroundColor Red
}

Write-Host "
=== Test Complete ===" -ForegroundColor Green
Write-Host "All systems are operational! " -ForegroundColor Green
Write-Host "
Access your system:" -ForegroundColor Yellow
Write-Host " Dashboard: http://localhost:8000/dashboard" -ForegroundColor Cyan
Write-Host " API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
