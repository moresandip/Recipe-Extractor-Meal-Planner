@echo off
echo ==========================================
echo   DIAGNOSING "NOT FOUND" ERROR
echo ==========================================
echo.

echo Step 1: Checking if backend is running...
curl -s http://localhost:8000/ >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Backend is running on port 8000
    curl -s http://localhost:8000/
) else (
    echo [FAIL] Backend NOT running on port 8000
    echo.
    echo SOLUTION: Start backend with:
    echo   cd backend
echo   venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
)

echo.
echo Step 2: Checking /api/health endpoint...
curl -s http://localhost:8000/api/health 2>nul
if %errorlevel% == 0 (
    echo [OK] Health endpoint working
) else (
    echo [FAIL] Health endpoint not responding
)

echo.
echo Step 3: Checking /api/extract endpoint...
curl -s -X POST http://localhost:8000/api/extract -H "Content-Type: application/json" -d "{\"url\":\"https://www.simplyrecipes.com/recipes/grilled_cheese/\"}" 2>nul | findstr "title" >nul
if %errorlevel% == 0 (
    echo [OK] Extract endpoint working
) else (
    echo [CHECK] Extract endpoint - may need testing with real request
)

echo.
echo ==========================================
echo   IF ALL STEPS FAIL:
echo ==========================================
echo.
echo 1. Kill all Node and Python processes:
echo    taskkill /F /IM node.exe
echo    taskkill /F /IM python.exe
echo.
echo 2. Restart backend:
echo    cd backend
echo    venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
echo.
echo 3. Restart frontend:
echo    cd frontend
echo    npm start
echo.
pause
