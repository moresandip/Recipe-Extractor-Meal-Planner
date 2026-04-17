@echo off
cd /d "%~dp0backend"
start cmd /k "venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3
cd /d "%~dp0frontend"
start cmd /k "npm start"
