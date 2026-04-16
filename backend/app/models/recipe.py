from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    title = Column(String(255), nullable=False)
    cuisine = Column(String(100), nullable=True)
    prep_time = Column(String(50), nullable=True)
    cook_time = Column(String(50), nullable=True)
    total_time = Column(String(50), nullable=True)
    servings = Column(Integer, nullable=True)
    difficulty = Column(String(20), nullable=True)
    ingredients = Column(JSON, nullable=False)
    instructions = Column(JSON, nullable=False)
    nutrition_estimate = Column(JSON, nullable=True)
    substitutions = Column(JSON, nullable=True)
    shopping_list = Column(JSON, nullable=True)
    related_recipes = Column(JSON, nullable=True)
    raw_html = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "cuisine": self.cuisine,
            "prep_time": self.prep_time,
            "cook_time": self.cook_time,
            "total_time": self.total_time,
            "servings": self.servings,
            "difficulty": self.difficulty,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "nutrition_estimate": self.nutrition_estimate,
            "substitutions": self.substitutions,
            "shopping_list": self.shopping_list,
            "related_recipes": self.related_recipes,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
