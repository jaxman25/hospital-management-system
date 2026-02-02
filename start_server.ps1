# Hospital Management System Server Starter
# Usage: .\start_server.ps1

Write-Host "=== Starting Hospital Management System ===" -ForegroundColor Cyan
Write-Host "Time: 02/02/2026 15:47:16" -ForegroundColor Gray
Write-Host ""

# Check if server is already running
$process = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn*" }
if ($process) {
    Write-Host " Server is already running (PID: $($process.Id))" -ForegroundColor Red
    Write-Host "Please stop it first with: Stop-Process -Id $($process.Id) -Force" -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting FastAPI server with Uvicorn..." -ForegroundColor Yellow

# Start the server
$serverProcess = Start-Process -NoNewWindow -PassThru python -ArgumentList "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"

# Wait a moment
Start-Sleep -Seconds 3

Write-Host " Server started (PID: $($serverProcess.Id))" -ForegroundColor Green
Write-Host ""

Write-Host "=== System Ready ===" -ForegroundColor Green
Write-Host "Access URLs:" -ForegroundColor Yellow
Write-Host "   Dashboard: http://localhost:8000/dashboard" -ForegroundColor Cyan
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "   Doctors API: http://localhost:8000/doctors/" -ForegroundColor Cyan
Write-Host "   Patients API: http://localhost:8000/patients/" -ForegroundColor Cyan
Write-Host "   Health Check: http://localhost:8000/api/health" -ForegroundColor Cyan
Write-Host ""

Write-Host "=== Management Commands ===" -ForegroundColor Yellow
Write-Host " Stop server: Press CTRL+C in this window" -ForegroundColor Gray
Write-Host " Force stop: Stop-Process -Id $($serverProcess.Id) -Force" -ForegroundColor Gray
Write-Host " Test API: .\quick_test.ps1" -ForegroundColor Gray
Write-Host " Create sample data: python create_sample_data.py" -ForegroundColor Gray
Write-Host ""

Write-Host "Server logs will appear below..." -ForegroundColor Gray
Write-Host "=========================================" -ForegroundColor DarkGray

# Wait for user to press CTRL+C
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
try {
    Wait-Process -Id $serverProcess.Id
} catch {
    Write-Host "Server stopped" -ForegroundColor Yellow
}
