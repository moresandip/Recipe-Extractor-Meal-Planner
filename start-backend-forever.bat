@echo off
echo Starting Backend Server...
echo This window must stay open!
cd /d "%~dp0backend"
:restart
venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
echo Backend crashed! Restarting in 5 seconds...
timeout /t 5
goto restart
