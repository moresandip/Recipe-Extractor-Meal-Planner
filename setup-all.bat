@echo off
echo ==========================================
echo SETTING UP BACKEND
echo ==========================================
cd /d "%~dp0backend"
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)
echo Installing Python packages...
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\pip install fastapi uvicorn sqlalchemy beautifulsoup4 requests langchain langchain-google-genai pydantic pydantic-settings python-dotenv httpx python-multipart
echo Backend setup complete!

echo.
echo ==========================================
echo SETTING UP FRONTEND
echo ==========================================
cd /d "%~dp0frontend"
if exist "node_modules" (
    echo Removing old node_modules...
    rmdir /s /q node_modules
)
if exist "package-lock.json" del package-lock.json
echo Installing npm packages...
npm install
echo Frontend setup complete!

echo.
echo ==========================================
echo SETUP COMPLETE! Now run:
echo   start-backend.bat
echo   start-frontend.bat
echo ==========================================
pause
