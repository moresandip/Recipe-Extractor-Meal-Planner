@echo off
echo ==========================================
echo   DEBUG TEST - Finding the Issue
echo ==========================================
echo.

cd /d "%~dp0backend"

echo [1] Testing with curl...
echo.

echo === Test 1: Health Check ===
curl -s http://localhost:8000/api/health
echo.
echo.

echo === Test 2: Debug Scrape ===
curl -s -X POST http://localhost:8000/api/debug/scrape -H "Content-Type: application/json" -d "{\"url\": \"https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/\"}"
echo.
echo.

echo === Test 3: Debug Full Extract ===
curl -s -X POST http://localhost:8000/api/debug/extract -H "Content-Type: application/json" -d "{\"url\": \"https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/\"}"
echo.
echo.

echo ==========================================
echo   Results:
echo ==========================================
echo.
echo If Test 1 fails: Backend is NOT running
echo If Test 2 fails: Website blocking scraper
echo If Test 3 fails: LLM/API key issue
echo.
pause
