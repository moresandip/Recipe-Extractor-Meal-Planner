#!/usr/bin/env python3
print("Starting import test...")

try:
    print("1. Importing FastAPI...")
    from fastapi import FastAPI
    print("   OK")
    
    print("2. Importing SQLAlchemy...")
    from sqlalchemy import create_engine
    print("   OK")
    
    print("3. Importing Pydantic...")
    from pydantic import BaseModel
    print("   OK")
    
    print("4. Importing BeautifulSoup...")
    from bs4 import BeautifulSoup
    print("   OK")
    
    print("5. Importing Requests...")
    import requests
    print("   OK")
    
    print("6. Importing LangChain...")
    from langchain_google_genai import ChatGoogleGenerativeAI
    print("   OK")
    
    print("7. Importing Cloudscraper...")
    import cloudscraper
    print("   OK")
    
    print("\n8. Importing app modules...")
    from app.core.config import settings
    print("   Config: OK")
    
    from app.core.database import engine, Base
    print("   Database: OK")
    
    from app.models.recipe import Recipe
    print("   Models: OK")
    
    from app.services.scraper import scraper
    print("   Scraper: OK")
    
    from app.services.llm_service import llm_service
    print("   LLM Service: OK")
    
    from app.main import app
    print("   Main App: OK")
    
    print("\n✅ ALL IMPORTS SUCCESSFUL!")
    print(f"API Key set: {'Yes' if settings.GEMINI_API_KEY else 'No'}")
    print(f"Database: {settings.DATABASE_URL}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\nPress Enter to exit...")
input()
