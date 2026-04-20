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
from app.services.smart_scraper import smart_scraper
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
    
    # Try scraping with multiple strategies
    scrape_result = scraper.scrape_url(url)
    
    # If first scraper fails, try smart scraper with multiple strategies
    if not scrape_result["success"]:
        logger.info("Primary scraper failed, trying smart scraper...")
        scrape_result = smart_scraper.scrape_url(url)
    
    if not scrape_result["success"]:
        error_msg = scrape_result["error"]
        logger.error(f"All scraping failed: {error_msg}")
        raise HTTPException(
            status_code=400, 
            detail=f"Unable to fetch recipe from URL. The website may be blocking automated access. Try a different recipe website like SimplyRecipes.com, FoodNetwork.com, or BonAppetit.com. Error: {error_msg}"
        )
    
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


SAMPLE_RECIPE = {
    "title": "Classic Grilled Cheese Sandwich",
    "cuisine": "American",
    "prep_time": "5 mins",
    "cook_time": "10 mins",
    "total_time": "15 mins",
    "servings": 1,
    "difficulty": "easy",
    "ingredients": [
        {"quantity": "2", "unit": "slices", "item": "bread"},
        {"quantity": "2", "unit": "slices", "item": "cheddar cheese"},
        {"quantity": "1", "unit": "tbsp", "item": "butter"}
    ],
    "instructions": [
        "Butter one side of each bread slice",
        "Place cheese between unbuttered sides",
        "Heat pan over medium heat",
        "Grill sandwich until golden brown on both sides",
        "Serve hot and enjoy!"
    ],
    "nutrition_estimate": {
        "calories": 350,
        "protein": "15g",
        "carbs": "30g",
        "fat": "18g"
    },
    "substitutions": [
        "Use mozzarella instead of cheddar for milder flavor",
        "Try sourdough bread for extra tanginess",
        "Use olive oil instead of butter for healthier option"
    ],
    "shopping_list": {
        "bakery": ["bread"],
        "dairy": ["cheddar cheese", "butter"]
    },
    "related_recipes": ["Tomato Soup", "French Fries", "Coleslaw"]
}


@router.post("/demo-extract")
def demo_extract(db: Session = Depends(get_db)):
    """
    Demo endpoint that returns sample recipe data for testing UI.
    """
    url = "https://demo.recipe.app/grilled-cheese"
    
    # Check if exists
    existing = db.query(Recipe).filter(Recipe.url == url).first()
    if existing:
        return existing.to_dict()
    
    # Create sample recipe
    recipe = Recipe(
        url=url,
        title=SAMPLE_RECIPE["title"],
        cuisine=SAMPLE_RECIPE["cuisine"],
        prep_time=SAMPLE_RECIPE["prep_time"],
        cook_time=SAMPLE_RECIPE["cook_time"],
        total_time=SAMPLE_RECIPE["total_time"],
        servings=SAMPLE_RECIPE["servings"],
        difficulty=SAMPLE_RECIPE["difficulty"],
        ingredients=SAMPLE_RECIPE["ingredients"],
        instructions=SAMPLE_RECIPE["instructions"],
        nutrition_estimate=SAMPLE_RECIPE["nutrition_estimate"],
        substitutions=SAMPLE_RECIPE["substitutions"],
        shopping_list=SAMPLE_RECIPE["shopping_list"],
        related_recipes=SAMPLE_RECIPE["related_recipes"],
        raw_html=""
    )
    
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    
    return recipe.to_dict()


@router.post("/debug/scrape")
def debug_scrape(request: RecipeExtractRequest):
    """
    Debug endpoint to test scraping only.
    """
    url = request.url
    logger.info(f"Debug scraping: {url}")
    
    scrape_result = scraper.scrape_url(url)
    
    return {
        "scrape_success": scrape_result["success"],
        "scrape_error": scrape_result.get("error"),
        "title": scrape_result.get("title"),
        "text_length": len(scrape_result.get("text_content", "")) if scrape_result["success"] else 0,
        "has_structured_data": bool(scrape_result.get("structured_data")) if scrape_result["success"] else False
    }


@router.post("/debug/extract")
def debug_extract(request: RecipeExtractRequest):
    """
    Debug endpoint to test LLM extraction only (requires scraping first).
    """
    url = request.url
    logger.info(f"Debug extract: {url}")
    
    # Scrape first
    scrape_result = scraper.scrape_url(url)
    if not scrape_result["success"]:
        return {
            "stage": "scraping",
            "success": False,
            "error": scrape_result["error"]
        }
    
    # Then test LLM
    text_content = scrape_result["text_content"][:3000]  # Limit for test
    llm_result = llm_service.extract_recipe(text_content, scrape_result.get("structured_data"))
    
    return {
        "stage": "llm_extraction",
        "scrape_success": True,
        "llm_success": llm_result["success"],
        "llm_error": llm_result.get("error"),
        "data_preview": llm_result.get("data", {}).get("title") if llm_result["success"] else None
    }
