import google.generativeai as genai
from app.core.config import settings
from typing import Dict, Any, List
import json
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use gemini-1.5-flash which is the correct model name
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def extract_recipe(self, scraped_content: str, structured_data: Dict = None) -> Dict[str, Any]:
        """Extract structured recipe data using LLM"""
        
        # Build the prompt
        context = f"""
You are a recipe extraction assistant. Extract structured recipe data from the following content.

PAGE CONTENT:
{scraped_content[:10000]}

"""
        
        if structured_data:
            context += f"\nSTRUCTURED DATA (if available):\n{json.dumps(structured_data, indent=2)}\n\n"
        
        context += """
Extract the following information in JSON format:
{{
    "title": "Recipe title",
    "cuisine": "Cuisine type (e.g., Italian, Mexican, American, Asian)",
    "prep_time": "Preparation time (e.g., 10 mins, 30 minutes)",
    "cook_time": "Cooking time (e.g., 20 mins, 1 hour)",
    "total_time": "Total time (prep + cook)",
    "servings": number of servings,
    "difficulty": "easy, medium, or hard based on complexity",
    "ingredients": [
        {{"quantity": "amount", "unit": "unit of measurement", "item": "ingredient name"}},
        ...
    ],
    "instructions": [
        "Step 1 description",
        "Step 2 description",
        ...
    ],
    "nutrition_estimate": {{
        "calories": approximate calories per serving (number),
        "protein": "protein amount with unit (e.g., 15g)",
        "carbs": "carbs amount with unit (e.g., 30g)",
        "fat": "fat amount with unit (e.g., 12g)"
    }},
    "substitutions": [
        "3 ingredient substitutions with reasoning",
    ],
    "shopping_list": {{
        "category_name": ["item1", "item2"],
        ...
    }},
    "related_recipes": [
        "3 recipe names that pair well with this dish"
    ]
}}

IMPORTANT RULES:
- Use ONLY information from the provided content
- If information is not available, use null or make reasonable estimates
- Group shopping items by logical categories (dairy, produce, pantry, meat, etc.)
- Ensure ingredients have quantity, unit, and item separated clearly
- Keep instructions clear and numbered
- Difficulty should be based on: easy (beginner-friendly, <30 min), medium (moderate skills, 30-60 min), hard (complex techniques, >60 min)
"""

        try:
            response = self.model.generate_content(context)
            content_text = response.text
            
            # Try to parse JSON from response
            # Handle potential markdown code blocks
            if "```json" in content_text:
                content_text = content_text.split("```json")[1].split("```")[0].strip()
            elif "```" in content_text:
                content_text = content_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content_text)
            
            # Ensure all required fields are present
            required_fields = ["title", "cuisine", "ingredients", "instructions"]
            for field in required_fields:
                if field not in result:
                    result[field] = None
            
            return {
                "success": True,
                "data": result
            }
            
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Failed to parse LLM response: {str(e)}",
                "raw_response": content_text if 'content_text' in locals() else None
            }
        except Exception as e:
            logger.error(f"LLM extraction failed: {str(e)}")
            return {
                "success": False,
                "error": f"LLM processing error: {str(e)}"
            }
    
    def generate_meal_plan(self, recipes: List[Dict]) -> Dict[str, Any]:
        """Generate a combined meal plan and shopping list from multiple recipes"""
        
        recipes_text = json.dumps(recipes, indent=2)
        
        prompt = f"""
You are a meal planning assistant. Create a combined meal plan from the following recipes.

RECIPES:
{recipes_text}

Generate:
1. A combined shopping list with merged quantities (grouped by category)
2. A weekly meal schedule
3. Prep tips for efficient cooking

Return in this JSON format:
{{
    "meal_plan": {{
        "monday": "Recipe name",
        "tuesday": "Recipe name",
        ...
    }},
    "combined_shopping_list": {{
        "category_name": ["item with quantity"],
        ...
    }},
    "prep_tips": ["tip 1", "tip 2", ...],
    "total_estimated_time": "total prep + cook time for all recipes"
}}
"""

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
                "error": f"Failed to generate meal plan: {str(e)}"
            }


llm_service = LLMService()
