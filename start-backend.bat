@echo off
cd /d "%~dp0backend"
if not exist "venv" (
    python -m venv venv
)
venv\Scripts\python -m pip install --upgrade pip -q
venv\Scripts\pip install -q fastapi uvicorn sqlalchemy beautifulsoup4 requests langchain langchain-google-genai pydantic pydantic-settings python-dotenv
venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
