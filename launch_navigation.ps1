Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  HOSPITAL NAVIGATION LAUNCHER            " -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

Write-Host "
 Launching Hospital Navigation Page..." -ForegroundColor Yellow

# Check if server is running
try {
    \ = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host " Server is running on http://localhost:8000" -ForegroundColor Green
} catch {
    Write-Host "  Server not detected on http://localhost:8000" -ForegroundColor Yellow
    Write-Host "   Starting server might be needed..." -ForegroundColor White
}

# Open navigation page
if (Test-Path "hospital_navigation.html") {
    Start-Process "hospital_navigation.html"
    Write-Host " Navigation page opened in browser" -ForegroundColor Green
} else {
    Write-Host " hospital_navigation.html not found" -ForegroundColor Red
}

Write-Host "
 Available Pages:" -ForegroundColor Cyan
Write-Host "    Navigation: hospital_navigation.html" -ForegroundColor White
Write-Host "    Dashboard: http://localhost:8000/dashboard" -ForegroundColor White
Write-Host "    API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "    Pharmacy: pharmacy-dashboard.html" -ForegroundColor White

Write-Host "
 Quick Access:" -ForegroundColor Yellow
Write-Host "   Press Ctrl+Click to open multiple pages" -ForegroundColor White
Write-Host "   F5 to refresh status in navigation page" -ForegroundColor White
