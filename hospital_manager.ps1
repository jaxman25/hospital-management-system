# ==========================================================
#  HOSPITAL MANAGEMENT SYSTEM - CONTROL PANEL
# ==========================================================

function Show-Menu {
    Clear-Host
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "  HOSPITAL MANAGEMENT SYSTEM CONTROL      " -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1.  Start Server" -ForegroundColor Yellow
    Write-Host "2.  Open Dashboard" -ForegroundColor Yellow
    Write-Host "3.  Open API Documentation" -ForegroundColor Yellow
    Write-Host "4.  Test API Endpoints" -ForegroundColor Yellow
    Write-Host "5.  Stop Server" -ForegroundColor Red
    Write-Host "6.  View System Status" -ForegroundColor Yellow
    Write-Host "7.  Project Information" -ForegroundColor Yellow
    Write-Host "8.  Exit" -ForegroundColor Red
    Write-Host ""
}

function Start-Server {
    Write-Host "Starting Hospital Management System..." -ForegroundColor Green
    Write-Host "Access URLs:" -ForegroundColor Cyan
    Write-Host "  Dashboard: http://localhost:8000/dashboard" -ForegroundColor White
    Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor White
    Write-Host "  Health:    http://localhost:8000/api/health" -ForegroundColor White
    Write-Host ""
    Write-Host "Press Ctrl+C in this window to stop the server" -ForegroundColor Red
    
    # Activate virtual environment if not already
    if (-not C:\Users\KONZA\Desktop\Project-2-HOSPITAL-MANAGMENT-SYSTEM\venv) {
        if (Test-Path "venv\Scripts\Activate.ps1") {
            .\venv\Scripts\Activate.ps1
        }
    }
    
    # Start the server
    python -m uvicorn minimal_main:app --reload --host 0.0.0.0 --port 8000
}

function Open-Dashboard {
    Write-Host "Opening Dashboard..." -ForegroundColor Green
    Start-Process "http://localhost:8000/dashboard"
}

function Open-API-Docs {
    Write-Host "Opening API Documentation..." -ForegroundColor Green
    Start-Process "http://localhost:8000/docs"
}

function Test-API {
    Write-Host "=== Testing API Endpoints ===" -ForegroundColor Cyan
    
     = @(
        @{Url="http://localhost:8000/api/health"; Name="Health Check"},
        @{Url="http://localhost:8000/api/doctors"; Name="Doctors API"},
        @{Url="http://localhost:8000/api/patients"; Name="Patients API"}
    )
    
    foreach ( in ) {
        try {
             = Invoke-WebRequest -Uri .Url -ErrorAction Stop
            Write-Host " : HTTP " -ForegroundColor Green
        } catch {
            Write-Host " : Not reachable" -ForegroundColor Red
        }
    }
}

function Stop-Server {
    Write-Host "Stopping server..." -ForegroundColor Yellow
    try {
        \ = Get-Process | Where-Object { \.Id -in (@(netstat -ano | findstr :8000) -replace '.*\s+(\d+)\$', '\') }
        if (\) {
            \ | ForEach-Object { Stop-Process -Id \$\_.Id -Force }
            Write-Host " Server stopped" -ForegroundColor Green
        } else {
            Write-Host "ℹ  No server running on port 8000" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  Error stopping server" -ForegroundColor Red
    }
    Pause
}

function Show-Status {
    Write-Host "=== System Status ===" -ForegroundColor Cyan
    
    # Check if server is running
    \ = \False
    try {
        \ = netstat -ano | findstr :8000
        if (\) {
            Write-Host " Server: RUNNING on port 8000" -ForegroundColor Green
            \ = \True
        } else {
            Write-Host " Server: NOT RUNNING" -ForegroundColor Red
        }
    } catch {
        Write-Host " Server: NOT RUNNING" -ForegroundColor Red
    }
    
    # Test endpoints if running
    if (\) {
        Write-Host ""
        Test-API
    }
    
    Pause
}

function Show-Project-Info {
    Write-Host "=== Project Information ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host " Hospital Management System" -ForegroundColor Green
    Write-Host "Built with FastAPI and Python" -ForegroundColor White
    Write-Host ""
    Write-Host " Project Location:" -ForegroundColor Yellow
    Write-Host "  \C:\Users\KONZA\Desktop\Project-2-HOSPITAL-MANAGMENT-SYSTEM" -ForegroundColor White
    Write-Host ""
    Write-Host " Available URLs:" -ForegroundColor Yellow
    Write-Host "  http://localhost:8000/dashboard" -ForegroundColor White
    Write-Host "  http://localhost:8000/docs" -ForegroundColor White
    Write-Host "  http://localhost:8000/api/health" -ForegroundColor White
    Write-Host "  http://localhost:8000/api/doctors" -ForegroundColor White
    Write-Host "  http://localhost:8000/api/patients" -ForegroundColor White
    Write-Host ""
    Write-Host " Quick Start:" -ForegroundColor Yellow
    Write-Host "  1. Run 'Start Server' from this menu" -ForegroundColor White
    Write-Host "  2. Open Dashboard or API Docs" -ForegroundColor White
    Write-Host "  3. Use the API as needed" -ForegroundColor White
    Write-Host ""
    Pause
}

# Main menu loop
do {
    Show-Menu
    \ = Read-Host "Please choose an option (1-8)"
    
    switch (\) {
        '1' { Start-Server }
        '2' { Open-Dashboard }
        '3' { Open-API-Docs }
        '4' { Test-API; Pause }
        '5' { Stop-Server }
        '6' { Show-Status }
        '7' { Show-Project-Info }
        '8' { 
            Write-Host "Exiting..." -ForegroundColor Yellow
            exit 0
        }
        default {
            Write-Host "Invalid selection. Please try again." -ForegroundColor Red
            Pause
        }
    }
} while (\True)
