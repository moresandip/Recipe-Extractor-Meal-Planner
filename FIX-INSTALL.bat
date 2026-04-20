@echo off
echo ==========================================
echo   FIXING MISSING DEPENDENCIES
echo ==========================================
echo.

cd /d "c:\Users\mores\OneDrive\Desktop\Recipe Extractor & Meal Planner\backend"

echo Installing google-generativeai...
venv\Scripts\pip install google-generativeai --upgrade

echo.
echo Installing other dependencies...
venv\Scripts\pip install requests beautifulsoup4 cloudscraper

echo.
echo Done! Now restart backend:
echo   cd backend
echo   venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
echo.
pause
