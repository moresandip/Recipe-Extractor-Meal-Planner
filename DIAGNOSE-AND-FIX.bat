@echo off
echo ==========================================
echo   DIAGNOSING BACKEND ISSUE
echo ==========================================
echo.

REM Kill old processes
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

echo [1] Checking if backend files exist...
cd /d "%~dp0backend"
if exist "venv\Scripts\python.exe" (
    echo Python venv: FOUND
) else (
    echo Python venv: NOT FOUND - Creating...
    python -m venv venv
)

echo.
echo [2] Installing ALL dependencies...
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\pip install fastapi uvicorn sqlalchemy beautifulsoup4 requests
venv\Scripts\pip install langchain langchain-google-genai pydantic pydantic-settings
venv\Scripts\pip install cloudscraper python-dotenv httpx python-multipart

echo.
echo [3] Testing backend import...
venv\Scripts\python -c "from app.main import app; print('Backend import: SUCCESS')" 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Backend import failed!
    echo Check error above ^
    pause
    exit /b
)

echo.
echo [4] Starting Backend with LOGGING...
start "BACKEND-LOG" cmd /k "cd /d %~dp0backend && venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 2>&1"

echo.
echo Waiting 8 seconds for backend...
timeout /t 8 /nobreak >nul

echo.
echo [5] Testing if backend is running...
curl -s http://localhost:8000/ > backend-test.txt 2>&1
if %errorlevel% equ 0 (
    echo Backend: RUNNING
type backend-test.txt
) else (
    echo Backend: NOT RESPONDING
    echo Check the BACKEND-LOG window for errors!
)

echo.
echo [6] Installing Frontend dependencies...
cd /d "%~dp0frontend"
if not exist "node_modules" (
    npm install
)

echo.
echo [7] Starting Frontend...
start "FRONTEND" cmd /k "npm start"

echo.
echo ==========================================
echo   SERVERS STARTED
echo ==========================================
echo.
echo Check BACKEND-LOG window for any errors!
echo.
echo Frontend will open at: http://localhost:3000
echo.
pause
