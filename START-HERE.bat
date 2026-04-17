@echo off
echo ==========================================
echo   RECIPE EXTRACTOR - AUTO START
echo ==========================================
echo.

REM Kill any existing processes first
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo [1/4] Installing Backend Dependencies...
cd /d "%~dp0backend"
venv\Scripts\pip install fastapi uvicorn sqlalchemy beautifulsoup4 requests langchain langchain-google-genai pydantic pydantic-settings python-dotenv httpx python-multipart -q 2>nul

echo [2/4] Starting Backend Server...
start "BACKEND - Port 8000" cmd /k "venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

echo [3/4] Installing Frontend Dependencies...
cd /d "%~dp0frontend"
if not exist "node_modules\react-scripts" (
    npm install
)

echo [4/4] Starting Frontend Server...
start "FRONTEND - Port 3000" cmd /k "npm start"

echo.
echo ==========================================
echo   SERVERS STARTED!
echo ==========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Wait 30 seconds for frontend to compile...
echo Then open: http://localhost:3000
echo.
echo DO NOT close this window!
pause
