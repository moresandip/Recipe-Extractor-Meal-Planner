@echo off
echo ==========================================
echo   TESTING BACKEND CONNECTION
echo ==========================================
echo.

echo Test 1: Checking if backend is running on port 8000...
curl -s http://localhost:8000/ >nul 2>&1
if %errorlevel% == 0 (
    echo [PASS] Backend is running!
    curl -s http://localhost:8000/
    echo.
) else (
    echo [FAIL] Backend NOT running on port 8000!
    echo.
    echo START BACKEND WITH:
    echo   cd backend
    echo   venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
    echo.
    pause
    exit /b 1
)

echo Test 2: Checking /api/health endpoint...
curl -s http://localhost:8000/api/health
echo.
echo.

echo Test 3: Testing recipe extraction with SimplyRecipes...
echo Sending request... (this may take 10-30 seconds)
curl -s -X POST http://localhost:8000/api/extract -H "Content-Type: application/json" -d "{\"url\":\"https://www.simplyrecipes.com/recipes/grilled_cheese/\"}"
echo.
echo.

echo ==========================================
echo   TEST COMPLETE
echo ==========================================
echo.
if %errorlevel% == 0 (
    echo If you see recipe data above, everything is working!
) else (
    echo If test failed, check:
    echo   1. Backend is running
    echo   2. Website is not blocking scrapers
    echo   3. Try a different recipe URL
)
echo.
pause
