@echo off
echo ==========================================
echo   RECIPE EXTRACTOR - STARTING APP
echo ==========================================
echo.

REM Check if backend venv exists, create if not
if not exist "backend\venv" (
    echo [1/5] Creating Python virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

REM Install backend dependencies
echo [2/5] Installing backend dependencies...
cd backend
venv\Scripts\pip install -q -r requirements.txt 2>nul
cd ..

REM Install frontend dependencies
echo [3/5] Installing frontend dependencies...
cd frontend
call npm install 2>nul
cd ..

echo.
echo [4/5] Starting Backend Server on http://localhost:8080
cd backend
start "Backend Server" cmd /k "venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload"
cd ..

echo [5/5] Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul

echo Starting Frontend Server on http://localhost:3000
cd frontend
start "Frontend Server" cmd /k "npm start"
cd ..

echo.
echo ==========================================
echo   SERVERS STARTED SUCCESSFULLY!
echo ==========================================
echo.
echo Backend API:  http://localhost:8080
echo Frontend:     http://localhost:3000
echo API Docs:     http://localhost:8080/docs
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak > nul

start http://localhost:3000

echo.
echo Press any key to STOP all servers...
pause > nul

taskkill /f /fi "WINDOWTITLE eq Backend Server" 2>nul
taskkill /f /fi "WINDOWTITLE eq Frontend Server" 2>nul
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul
echo Servers stopped!
