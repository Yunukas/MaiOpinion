# Start MaiOpinion Application
# This script starts both backend and frontend servers

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "MaiOpinion - AI Medical Diagnostic System" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "[WARNING] .env file not found!" -ForegroundColor Yellow
    Write-Host "Please create a .env file with your GITHUB_TOKEN" -ForegroundColor Yellow
    Write-Host ""
}

# Start Backend Server
Write-Host "[1/2] Starting Backend API Server..." -ForegroundColor Green
Write-Host "      Location: http://localhost:5000" -ForegroundColor Gray
Write-Host ""

$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    & "$using:PWD\.venv\Scripts\python.exe" api_server.py
}

Start-Sleep -Seconds 3

# Check if frontend exists
if (-not (Test-Path "frontend")) {
    Write-Host "[ERROR] Frontend directory not found!" -ForegroundColor Red
    Write-Host "Please ensure frontend is properly set up" -ForegroundColor Red
    Stop-Job $backendJob
    Remove-Job $backendJob
    exit 1
}

# Start Frontend Server
Write-Host "[2/2] Starting Frontend Development Server..." -ForegroundColor Green
Write-Host "      Location: http://localhost:3000" -ForegroundColor Gray
Write-Host ""

Set-Location frontend

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "      Installing frontend dependencies..." -ForegroundColor Yellow
    npm install
    Write-Host ""
}

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "Application is starting!" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:  http://localhost:5000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop both servers" -ForegroundColor Yellow
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

# Start frontend (this will be the foreground process)
npm run dev

# Cleanup when frontend stops
Stop-Job $backendJob
Remove-Job $backendJob
Write-Host "Servers stopped." -ForegroundColor Red
