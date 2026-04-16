@echo off
chcp 65001 >nul
echo ==========================================
echo   RECIPE EXTRACTOR - FULL SETUP
echo ==========================================
echo.

REM Kill any existing processes
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak > nul

echo Step 1: Setting up Backend...
cd /d "%~dp0backend"

if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Installing backend dependencies...
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\pip install fastapi uvicorn sqlalchemy beautifulsoup4 requests langchain langchain-google-genai pydantic pydantic-settings python-dotenv

echo.
echo Step 2: Setting up Frontend...
cd /d "%~dp0frontend"

if exist "node_modules" (
    echo Removing old node_modules...
    rmdir /s /q node_modules 2>nul
)
if exist "package-lock.json" (
    del package-lock.json 2>nul
)

echo Installing frontend dependencies (this may take 2-3 minutes)...
call npm install

echo.
echo ==========================================
echo   STARTING SERVERS
echo ==========================================
echo.

echo Starting Backend on http://localhost:8000
cd /d "%~dp0backend"
start "BACKEND" cmd /k "venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo Waiting 5 seconds for backend...
timeout /t 5 /nobreak > nul

echo Starting Frontend on http://localhost:3000
cd /d "%~dp0frontend"
start "FRONTEND" cmd /k "npm start"

echo.
echo ==========================================
echo   APP IS STARTING!
echo ==========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Wait 15 seconds for frontend to compile...
echo.
pause
