@echo off
echo Starting Recipe Extractor Application...
echo.

REM Start Backend
echo Starting Backend Server on http://localhost:8000
cd /d "%~dp0backend"
start "Backend Server" cmd /c "venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 5 /nobreak > nul

REM Start Frontend
echo Starting Frontend Server on http://localhost:3000
cd /d "%~dp0frontend"
start "Frontend Server" cmd /c "npm start"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to stop all servers...
pause > nul

taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul
