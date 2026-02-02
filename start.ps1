Write-Host "Starting Hospital Management System..." -ForegroundColor Green
Write-Host "Access: http://localhost:8000" -ForegroundColor Yellow
uvicorn main:app --host 0.0.0.0 --port 8000
