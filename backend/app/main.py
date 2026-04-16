from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import routes

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Recipe Extractor & Meal Planner API",
    description="Extract recipes from URLs using LLM and generate meal plans",
    version="1.0.0"
)

# CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router, prefix="/api", tags=["recipes"])

@app.get("/")
def root():
    return {
        "message": "Recipe Extractor & Meal Planner API",
        "docs": "/docs",
        "version": "1.0.0"
    }
