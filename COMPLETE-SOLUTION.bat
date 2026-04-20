@echo off
echo ==========================================
echo   RECIPE EXTRACTOR - COMPLETE SOLUTION
echo ==========================================
echo.
echo This will start both backend and frontend
echo.

REM Kill any old processes
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

cd /d "%~dp0"

echo [1/4] Installing backend dependencies...
cd backend
venv\Scripts\python -m pip install --upgrade pip -q 2>nul
venv\Scripts\pip install -q requests beautifulsoup4 cloudscraper 2>nul

echo [2/4] Starting Backend Server...
start "BACKEND - Port 8000" cmd /k "cd /d %~dp0backend && venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo [3/4] Waiting for backend to start (10 seconds)...
timeout /t 10 /nobreak >nul

echo [4/4] Starting Frontend Server...
cd /d "%~dp0frontend"
start "FRONTEND - Port 3000" cmd /k "npm start"

echo.
echo ==========================================
echo   SERVERS STARTED SUCCESSFULLY!
echo ==========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo INSTRUCTIONS:
echo 1. Wait 30 seconds for frontend to compile
echo 2. Open browser: http://localhost:3000
echo 3. Enter any recipe URL and click "Extract Recipe"
echo.
echo If a website blocks scraping, try:
echo - Different recipe website
echo - Wait a few seconds and retry
echo - The app will automatically try 4 different methods
echo.
pause
