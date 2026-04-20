@echo off
echo ==========================================
echo   RECIPE EXTRACTOR - FINAL SOLUTION
echo ==========================================
echo.
echo This will start both backend and frontend
echo.

REM Kill any old processes
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

cd /d "%~dp0"

echo [1] Checking backend dependencies...
cd backend
venv\Scripts\pip install -q google-generativeai 2>nul

echo.
echo [2] Starting Backend Server...
start "BACKEND - Port 8000" cmd /k "cd /d %~dp0backend && venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo.
echo Waiting 8 seconds for backend...
timeout /t 8 /nobreak >nul

echo [3] Checking backend health...
curl -s http://localhost:8000/api/health >nul
if %errorlevel% neq 0 (
    echo WARNING: Backend may not be ready yet
) else (
    echo Backend: OK
)

echo.
echo [4] Starting Frontend Server...
cd /d "%~dp0frontend"
start "FRONTEND - Port 3000" cmd /k "npm start"

echo.
echo ==========================================
echo   SERVERS STARTING...
echo ==========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Wait 30 seconds for frontend to compile
echo.
echo If you see "Not Found" error:
echo   1. Try the "Demo Mode" button in the UI
echo   2. Or use a different recipe website URL
echo.
pause
