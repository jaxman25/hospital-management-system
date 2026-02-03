Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  HOSPITAL MANAGEMENT SYSTEM - FASTAPI    " -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

# Check virtual environment
if (-not C:\Users\KONZA\Desktop\Project-2-HOSPITAL-MANAGMENT-SYSTEM\venv) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    if (Test-Path "venv\Scripts\Activate.ps1") {
        .\venv\Scripts\Activate.ps1
    }
}

Write-Host "
1. Checking dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "
2. Initializing database..." -ForegroundColor Yellow
try {
    python -c "
import sys
sys.path.append('.')
from backend.database import Base, engine
from backend.models import *
Base.metadata.create_all(bind=engine)
print(' Database tables created')
"
} catch {
    Write-Host "  Database already exists or error occurred" -ForegroundColor Yellow
}

Write-Host "
3. Creating sample data..." -ForegroundColor Yellow
if (Test-Path "create_sample_data.py") {
    python create_sample_data.py
}

Write-Host "
4. Starting FastAPI server..." -ForegroundColor Green
Write-Host "    Local URL:    http://localhost:8000" -ForegroundColor Cyan
Write-Host "    API Docs:     http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "    ReDoc:        http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host "
   Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host "   =========================================" -ForegroundColor Cyan

# Start the server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
