from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db
from app.models.recipe import Recipe
from app.api.schemas import (
    RecipeCreate, RecipeResponse, RecipeListItem, 
    MealPlanRequest, MealPlanResponse, ErrorResponse, RecipeExtractRequest
)
from app.services.scraper import scraper
from app.services.llm_service import llm_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/extract", response_model=RecipeResponse)
def extract_recipe(
    request: RecipeExtractRequest,
    db: Session = Depends(get_db)
):
    """
    Extract recipe from URL, process with LLM, and save to database.
    """
    url = request.url
    
    # Check if recipe already exists
    existing = db.query(Recipe).filter(Recipe.url == url).first()
    if existing:
        return existing.to_dict()
    
    # Scrape the URL
    scrape_result = scraper.scrape_url(url)
    
    if not scrape_result["success"]:
        raise HTTPException(status_code=400, detail=scrape_result["error"])
    
    # Extract recipe using LLM
    llm_result = llm_service.extract_recipe(
        scrape_result["text_content"],
        scrape_result.get("structured_data")
    )
    
    if not llm_result["success"]:
        logger.error(f"LLM extraction failed: {llm_result.get('error')}")
        raise HTTPException(status_code=500, detail=llm_result["error"])
    
    data = llm_result["data"]
    
    # Create recipe record
    recipe = Recipe(
        url=url,
        title=data.get("title", "Unknown Recipe"),
        cuisine=data.get("cuisine"),
        prep_time=data.get("prep_time"),
        cook_time=data.get("cook_time"),
        total_time=data.get("total_time"),
        servings=data.get("servings"),
        difficulty=data.get("difficulty"),
        ingredients=data.get("ingredients", []),
        instructions=data.get("instructions", []),
        nutrition_estimate=data.get("nutrition_estimate"),
        substitutions=data.get("substitutions", []),
        shopping_list=data.get("shopping_list", {}),
        related_recipes=data.get("related_recipes", []),
        raw_html=scrape_result.get("html", "")[:50000]  # Store limited HTML
    )
    
    try:
        db.add(recipe)
        db.commit()
        db.refresh(recipe)
        return recipe.to_dict()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save recipe: {str(e)}")


@router.get("/recipes", response_model=List[RecipeListItem])
def list_recipes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all saved recipes with pagination.
    """
    recipes = db.query(Recipe).order_by(Recipe.created_at.desc()).offset(skip).limit(limit).all()
    return [recipe.to_dict() for recipe in recipes]


@router.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific recipe by ID.
    """
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe.to_dict()


@router.delete("/recipes/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a recipe by ID.
    """
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    db.delete(recipe)
    db.commit()
    return {"message": "Recipe deleted successfully"}


@router.post("/meal-plan", response_model=MealPlanResponse)
def create_meal_plan(
    request: MealPlanRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a meal plan from selected recipe IDs.
    """
    if len(request.recipe_ids) < 1:
        raise HTTPException(status_code=400, detail="At least one recipe is required")
    
    if len(request.recipe_ids) > 7:
        raise HTTPException(status_code=400, detail="Maximum 7 recipes allowed for meal plan")
    
    # Fetch recipes
    recipes = []
    for recipe_id in request.recipe_ids:
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} not found")
        
        recipes.append({
            "id": recipe.id,
            "title": recipe.title,
            "ingredients": recipe.ingredients,
            "servings": recipe.servings
        })
    
    # Generate meal plan
    result = llm_service.generate_meal_plan(recipes)
    
    return result


@router.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
