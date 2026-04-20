@echo off
echo ==========================================
echo   RECIPE EXTRACTOR - FULL START
echo ==========================================
echo.

REM Kill any existing processes
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

cd /d "%~dp0backend"

echo [1/5] Installing critical packages first...
venv\Scripts\pip install google-generativeai --quiet 2>nul
venv\Scripts\pip install requests beautifulsoup4 cloudscraper --quiet 2>nul

echo [2/5] Installing other packages...
venv\Scripts\pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings --quiet 2>nul

echo.
echo [3/5] Starting Backend Server...
start "BACKEND-SERVER - Port 8080" cmd /k "venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload"

echo.
echo [4/5] Waiting 15 seconds for backend to fully start...
timeout /t 15 /nobreak >nul

echo [5/5] Checking backend status...
cd /d "%~dp0"
curl -s http://localhost:8080/api/health > check.txt 2>&1
findstr "healthy" check.txt >nul
if %errorlevel% equ 0 (
    echo ✅ Backend is RUNNING on port 8080
) else (
    echo ⚠️  Backend may still be starting...
    echo    If you see 'CANNOT CONNECT' error, wait 10 more seconds and refresh browser
)

echo.
echo ==========================================
echo   STARTING FRONTEND...
echo ==========================================
cd /d "%~dp0frontend"
if not exist "node_modules" (
    echo Installing npm packages (first time only)...
    npm install
)
start "FRONTEND-SERVER - Port 3000" cmd /k "npm start"

echo.
echo ==========================================
echo   ALL SERVERS STARTING!
echo ==========================================
echo.
echo 📱 Frontend: http://localhost:3000
echo ⚙️  Backend:  http://localhost:8080
echo.
echo ⏳ Wait 30 seconds for everything to load
echo 🔄 Then open http://localhost:3000 in browser
echo.
pause
