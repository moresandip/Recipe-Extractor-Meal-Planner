import google.generativeai as genai
from app.core.config import settings
from typing import Dict, Any, List
import json
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use models/gemini-1.5-flash which is the standard name
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    def extract_recipe(self, scraped_content: str, structured_data: Dict = None) -> Dict[str, Any]:
        """Extract structured recipe data using LLM"""
        
        prompt = f"""Extract structured recipe data from the following content.

PAGE CONTENT:
{scraped_content[:10000]}

"""
        
        if structured_data:
            prompt += f"\nSTRUCTURED DATA:\n{json.dumps(structured_data, indent=2)}\n\n"
        
        prompt += """Return ONLY a JSON object with this exact structure:
{
    "title": "Recipe title",
    "cuisine": "Cuisine type",
    "prep_time": "Preparation time",
    "cook_time": "Cooking time", 
    "total_time": "Total time",
    "servings": 4,
    "difficulty": "easy",
    "ingredients": [
        {"quantity": "1", "unit": "cup", "item": "flour"}
    ],
    "instructions": ["Step 1", "Step 2"],
    "nutrition_estimate": {
        "calories": 300,
        "protein": "10g",
        "carbs": "40g", 
        "fat": "12g"
    },
    "substitutions": ["Use milk instead of cream"],
    "shopping_list": {
        "produce": ["tomatoes"],
        "dairy": ["milk"]
    },
    "related_recipes": ["Garlic Bread"]
}"""

        try:
            response = self.model.generate_content(prompt)
            content_text = response.text
            
            # Parse JSON
            if "```json" in content_text:
                content_text = content_text.split("```json")[1].split("```")[0].strip()
            elif "```" in content_text:
                content_text = content_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content_text)
            
            return {
                "success": True,
                "data": result
            }
            
        except Exception as e:
            logger.error(f"LLM extraction failed: {str(e)}")
            return {
                "success": False,
                "error": f"LLM processing error: {str(e)}"
            }
    
    def generate_meal_plan(self, recipes: List[Dict]) -> Dict[str, Any]:
        """Generate a combined meal plan"""
        
        prompt = f"""Create a meal plan from these recipes:
{json.dumps(recipes, indent=2)}

Return ONLY JSON:
{{
    "meal_plan": {{"monday": "Recipe", "tuesday": "Recipe"}},
    "combined_shopping_list": {{"category": ["items"]}},
    "prep_tips": ["tip 1"],
    "total_estimated_time": "2 hours"
}}"""

        try:
            response = self.model.generate_content(prompt)
            content_text = response.text
            
            if "```json" in content_text:
                content_text = content_text.split("```json")[1].split("```")[0].strip()
            elif "```" in content_text:
                content_text = content_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content_text)
            
            return {
                "success": True,
                "data": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed: {str(e)}"
            }


llm_service = LLMService()
