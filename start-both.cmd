@echo off
cd /d "%~dp0backend"
start "BACKEND" cmd /c "venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
timeout /t 5
cd /d "%~dp0frontend"
start "FRONTEND" cmd /c "npm start"
