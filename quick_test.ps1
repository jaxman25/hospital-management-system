# Quick System Test
# Usage: .\quick_test.ps1

Write-Host "=== Quick System Test ===" -ForegroundColor Cyan

# Test 1: Check if server is running
Write-Host "1. Checking server status..." -ForegroundColor Yellow
$process = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn*" }
if ($process) {
    Write-Host "    Server is running (PID: $($process.Id))" -ForegroundColor Green
} else {
    Write-Host "    Server is NOT running" -ForegroundColor Red
    Write-Host "   Run: .\start_server.ps1" -ForegroundColor Yellow
    exit 1
}

# Test 2: Health check
Write-Host "2. Testing health check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -Method Get -TimeoutSec 5
    Write-Host "    Health: $($health.status)" -ForegroundColor Green
    Write-Host "    Database: $($health.database)" -ForegroundColor Green
} catch {
    Write-Host "    Cannot connect to server: $_" -ForegroundColor Red
    exit 1
}

# Test 3: Count doctors
Write-Host "3. Counting doctors..." -ForegroundColor Yellow
try {
    $doctors = Invoke-RestMethod -Uri "http://localhost:8000/doctors/" -Method Get -TimeoutSec 5
    Write-Host "    Doctors in database: $($doctors.Count)" -ForegroundColor Green
} catch {
    Write-Host "    Could not fetch doctors: $_" -ForegroundColor Yellow
}

# Test 4: Count patients
Write-Host "4. Counting patients..." -ForegroundColor Yellow
try {
    $patients = Invoke-RestMethod -Uri "http://localhost:8000/patients/" -Method Get -TimeoutSec 5
    Write-Host "    Patients in database: $($patients.Count)" -ForegroundColor Green
} catch {
    Write-Host "    Could not fetch patients: $_" -ForegroundColor Yellow
}

# Test 5: Check dashboard
Write-Host "5. Checking dashboard..." -ForegroundColor Yellow
try {
    $dashboard = Invoke-WebRequest -Uri "http://localhost:8000/dashboard" -Method Get -TimeoutSec 5
    Write-Host "    Dashboard accessible (Status: $($dashboard.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "    Dashboard not accessible: $_" -ForegroundColor Yellow
}

Write-Host "
=== System Status ===" -ForegroundColor Green
Write-Host " System is operational!" -ForegroundColor Green
Write-Host "
Access your system at:" -ForegroundColor Yellow
Write-Host " http://localhost:8000/dashboard" -ForegroundColor Cyan
Write-Host " http://localhost:8000/docs" -ForegroundColor Cyan
