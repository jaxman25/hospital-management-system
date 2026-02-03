Write-Host "=== HOSPITAL MANAGEMENT SYSTEM (FastAPI) ===" -ForegroundColor Cyan
Write-Host "Starting server..." -ForegroundColor Yellow

# Activate virtual environment if not already
if (-not ) {
    if (Test-Path "venv\Scripts\Activate.ps1") {
        .\venv\Scripts\Activate.ps1
    }
}

# Install dependencies if needed
if (Test-Path "requirements.txt") {
    Write-Host "Checking dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
python -c "
from backend.database import Base, engine
from backend.models import *
Base.metadata.create_all(bind=engine)
print('Database ready')
"

# Start the server
Write-Host "
 Server starting..." -ForegroundColor Green
Write-Host " Local:    http://localhost:8000" -ForegroundColor Cyan
Write-Host " API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host " Redoc:    http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host "
Press Ctrl+C to stop the server" -ForegroundColor Red

cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
