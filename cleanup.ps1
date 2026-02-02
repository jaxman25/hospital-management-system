# PowerShell script to clean up Python cache files
Write-Host "Cleaning Python cache files..." -ForegroundColor Yellow

# Remove __pycache__ directories
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Write-Host "Removed __pycache__ directories" -ForegroundColor Green

# Remove .pyc files
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
Write-Host "Removed .pyc files" -ForegroundColor Green

# Remove .pyo files
Get-ChildItem -Recurse -Filter "*.pyo" | Remove-Item -Force
Write-Host "Removed .pyo files" -ForegroundColor Green

# Remove .pyd files
Get-ChildItem -Recurse -Filter "*.pyd" | Remove-Item -Force
Write-Host "Removed .pyd files" -ForegroundColor Green

Write-Host "Cleanup complete!" -ForegroundColor Green
