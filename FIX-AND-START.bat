@echo off
echo ==========================================
echo   RECIPE EXTRACTOR - COMPLETE FIX
echo ==========================================
echo.

REM Step 1: Kill any old processes
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

echo [1/5] Checking Python packages...
cd /d "%~dp0backend"
venv\Scripts\python -m pip install --upgrade pip -q
venv\Scripts\pip install -q fastapi uvicorn sqlalchemy beautifulsoup4 requests
venv\Scripts\pip install -q langchain langchain-google-genai pydantic pydantic-settings
venv\Scripts\pip install -q cloudscraper python-dotenv httpx

echo [2/5] Checking Frontend packages...
cd /d "%~dp0frontend"
if not exist "node_modules" (
    echo Installing npm packages (wait 2-3 minutes)...
    npm install
)

echo [3/5] Starting Backend...
cd /d "%~dp0backend"
start "BACKEND" cmd /k "venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

echo [4/5] Testing backend...
curl -s http://localhost:8000/ >nul
if %errorlevel% neq 0 (
    echo Backend not responding yet, waiting more...
    timeout /t 5 >nul
)

echo [5/5] Starting Frontend...
cd /d "%~dp0frontend"
start "FRONTEND" cmd /k "npm start"

echo.
echo ==========================================
echo   DONE! Servers are starting...
echo ==========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Wait 20-30 seconds, then open browser
echo.
pause
