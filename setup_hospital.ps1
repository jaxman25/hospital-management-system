Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  HOSPITAL MANAGEMENT SYSTEM SETUP        " -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

# Step 1: Check Python
Write-Host "
1. Checking Python..." -ForegroundColor Yellow
python --version

# Step 2: Activate virtual environment
Write-Host "
2. Setting up virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    Write-Host "    Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "   Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    .\venv\Scripts\Activate.ps1
}

# Step 3: Install dependencies
Write-Host "
3. Installing dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host "    Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "   Installing core packages..." -ForegroundColor Cyan
    pip install fastapi uvicorn sqlalchemy python-dotenv requests
}

# Step 4: Initialize database
Write-Host "
4. Initializing database..." -ForegroundColor Yellow
try {
    python -c "
import sys
sys.path.append('.')
from backend.database import Base, engine
from backend.models import *
Base.metadata.create_all(bind=engine)
print('Database tables created')
"
    Write-Host "    Database initialized" -ForegroundColor Green
} catch {
    Write-Host "     Database already exists or minor error" -ForegroundColor Yellow
}

# Step 5: Create sample data
Write-Host "
5. Creating sample data..." -ForegroundColor Yellow
if (Test-Path "create_sample_data.py") {
    python create_sample_data.py
    Write-Host "    Sample data created" -ForegroundColor Green
}

# Step 6: Start server
Write-Host "
6. Starting Hospital Management System..." -ForegroundColor Green
Write-Host "    Dashboard: http://localhost:8000" -ForegroundColor Cyan
Write-Host "    API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "    Health:    http://localhost:8000/api/health" -ForegroundColor Cyan
Write-Host "
   Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host "   =========================================" -ForegroundColor Cyan

# Start the server
python -m uvicorn main_fixed:app --reload --host 0.0.0.0 --port 8000
