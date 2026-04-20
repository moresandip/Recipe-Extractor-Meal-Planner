@echo off
echo ==========================================
echo   TESTING RECIPE EXTRACTOR SYSTEM
echo ==========================================
echo.

cd /d "%~dp0backend"

echo [1] Installing google-generativeai package...
venv\Scripts\pip install google-generativeai==0.8.3 -q

echo.
echo [2] Running system test...
venv\Scripts\python test-scrape.py

echo.
echo ==========================================
echo   If test passed, restart your servers:
echo ==========================================
echo.
echo 1. Stop backend (CTRL+C)
echo 2. Restart: venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
echo 3. Refresh frontend
echo.
pause
