@echo off
chcp 65001 >nul
echo ==========================================
echo   RECIPE EXTRACTOR - FULL START
echo ==========================================
echo.

REM Kill existing processes
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul
timeout /t 3 /nobreak > nul

echo [1/6] Checking Python virtual environment...
cd /d "%~dp0backend"
if not exist "venv\Scripts\python.exe" (
    echo Creating new virtual environment...
    python -m venv venv
)

echo [2/6] Installing backend packages (wait 1-2 minutes)...
venv\Scripts\python -m pip install --upgrade pip -q
venv\Scripts\pip install fastapi uvicorn[standard] sqlalchemy beautifulsoup4 requests -q
venv\Scripts\pip install langchain langchain-google-genai pydantic pydantic-settings python-dotenv -q
venv\Scripts\pip install httpx python-multipart -q

echo [3/6] Testing backend import...
venv\Scripts\python -c "from app.main import app; print('Backend OK')" 2>nul
if errorlevel 1 (
    echo Backend import failed, but continuing...
)

echo [4/6] Installing frontend packages (wait 2-3 minutes)...
cd /d "%~dp0frontend"
if not exist "node_modules\react-scripts" (
    npm install
) else (
    echo Frontend packages already installed
)

echo.
echo [5/6] Starting Backend Server...
cd /d "%~dp0backend"
start "BACKEND-SERVER" cmd /k "venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo Waiting 5 seconds for backend...
timeout /t 5 /nobreak > nul

echo.
echo [6/6] Starting Frontend Server...
cd /d "%~dp0frontend"
start "FRONTEND-SERVER" cmd /k "npm start"

echo.
echo ==========================================
echo   SERVERS STARTING!
echo ==========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Wait 20 seconds, then open browser
echo.
pause
