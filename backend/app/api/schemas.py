from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime


class Ingredient(BaseModel):
    quantity: str
    unit: str
    item: str


class NutritionEstimate(BaseModel):
    calories: Optional[int] = None
    protein: Optional[str] = None
    carbs: Optional[str] = None
    fat: Optional[str] = None


class RecipeCreate(BaseModel):
    url: str


class RecipeResponse(BaseModel):
    id: int
    url: str
    title: str
    cuisine: Optional[str] = None
    prep_time: Optional[str] = None
    cook_time: Optional[str] = None
    total_time: Optional[str] = None
    servings: Optional[int] = None
    difficulty: Optional[str] = None
    ingredients: List[Dict[str, Any]]
    instructions: List[str]
    nutrition_estimate: Optional[NutritionEstimate] = None
    substitutions: Optional[List[str]] = []
    shopping_list: Optional[Dict[str, List[str]]] = {}
    related_recipes: Optional[List[str]] = []
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class RecipeListItem(BaseModel):
    id: int
    url: str
    title: str
    cuisine: Optional[str] = None
    difficulty: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


class MealPlanRequest(BaseModel):
    recipe_ids: List[int]


class MealPlanResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ErrorResponse(BaseModel):
    detail: str


class RecipeExtractRequest(BaseModel):
    url: str
