from app.core.config import settings
from typing import Dict, Any, List
import json
import logging

logger = logging.getLogger(__name__)

# Try to import google.generativeai, fallback to mock if not available
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    logger.error("google-generativeai not installed. Run: pip install google-generativeai")
    GENAI_AVAILABLE = False
    genai = None

class LLMService:
    def __init__(self):
        if not GENAI_AVAILABLE:
            logger.error("Google Generative AI not available. Recipe extraction will use fallback.")
            self.model = None
            return
        
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Try multiple model names - stable ones first
            model_names = [
                'gemini-1.5-flash',           # Most stable, widely available
                'gemini-1.5-flash-latest',    # Latest 1.5 version
                'gemini-1.5-pro',             # Pro version
                'gemini-pro',                 # Older stable
                'models/gemini-1.5-flash',    # Full path format
                'models/gemini-pro',          # Full path format
            ]
            
            for model_name in model_names:
                try:
                    logger.info(f"Trying model: {model_name}")
                    self.model = genai.GenerativeModel(model_name)
                    # Test the model with a simple call
                    self.model.generate_content("Hello")
                    logger.info(f"Successfully initialized model: {model_name}")
                    break
                except Exception as e:
                    logger.warning(f"Model {model_name} failed: {str(e)}")
                    continue
            else:
                logger.error("All Gemini models failed to initialize")
                self.model = None
                
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {str(e)}")
            self.model = None
    
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
{
    "title": "Recipe title",
    "cuisine": "Cuisine type (e.g., Italian, Mexican, American, Asian)",
    "prep_time": "Preparation time (e.g., 10 mins, 30 minutes)",
    "cook_time": "Cooking time (e.g., 20 mins, 1 hour)",
    "total_time": "Total time (prep + cook)",
    "servings": number of servings,
    "difficulty": "easy, medium, or hard based on complexity",
    "ingredients": [
        {"quantity": "amount", "unit": "unit of measurement", "item": "ingredient name"},
        ...
    ],
    "instructions": [
        "Step 1 description",
        "Step 2 description",
        ...
    ],
    "nutrition_estimate": {
        "calories": approximate calories per serving (number),
        "protein": "protein amount with unit (e.g., 15g)",
        "carbs": "carbs amount with unit (e.g., 30g)",
        "fat": "fat amount with unit (e.g., 12g)"
    },
    "substitutions": [
        "3 ingredient substitutions with reasoning",
    ],
    "shopping_list": {
        "category_name": ["item1", "item2"],
        ...
    },
    "related_recipes": [
        "3 recipe names that pair well with this dish"
    ]
}

IMPORTANT RULES:
- Use ONLY information from the provided content
- If information is not available, use null or make reasonable estimates
- Group shopping items by logical categories (dairy, produce, pantry, meat, etc.)
- Ensure ingredients have quantity, unit, and item separated clearly
- Keep instructions clear and numbered
- Difficulty should be based on: easy (beginner-friendly, <30 min), medium (moderate skills, 30-60 min), hard (complex techniques, >60 min)
"""

        if self.model is None:
            logger.warning("LLM model not available. Using simple extraction fallback.")
            return self._simple_extract(scraped_content, structured_data)
        
        try:
            response = self.model.generate_content(context)
            content_text = response.text
            
            # Parse JSON from response
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
            logger.warning(f"Failed to parse LLM response, using fallback: {str(e)}")
            return self._simple_extract(scraped_content, structured_data)
        except Exception as e:
            logger.error(f"LLM extraction failed: {str(e)}. Using fallback.")
            return self._simple_extract(scraped_content, structured_data)
    
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
    
    def _simple_extract(self, scraped_content: str, structured_data: Dict = None) -> Dict[str, Any]:
        """Simple regex-based extraction when LLM is not available"""
        import re
        
        logger.info("Using simple extraction fallback")
        
        # Try to extract title
        title = "Unknown Recipe"
        lines = scraped_content.split('\n')
        for line in lines[:20]:  # Check first 20 lines
            line = line.strip()
            if line and len(line) > 5 and len(line) < 100:
                # Skip common non-title lines
                if not any(skip in line.lower() for skip in ['login', 'sign up', 'menu', 'search', 'home', 'about', 'contact']):
                    title = line
                    break
        
        # Try to extract ingredients
        ingredients = []
        ingredient_patterns = [
            r'(?i)(\d+(?:/\d+)?(?:\.\d+)?)\s*(cup|cups|tbsp|tsp|oz|ounce|pound|lb|g|gram|kg|ml|l|pcs|piece|pieces|clove|cloves|pinch|dash)?\s+(.+)',
            r'(?i)(\d+)\s+(\w+)\s+(.+)'
        ]
        
        for line in lines:
            line = line.strip()
            if any(marker in line.lower() for marker in ['ingredient', '•', '-', '*']):
                for pattern in ingredient_patterns:
                    match = re.search(pattern, line)
                    if match:
                        ingredients.append({
                            "quantity": match.group(1) if match.groups() else "1",
                            "unit": match.group(2) if len(match.groups()) > 1 else "",
                            "item": match.group(3) if len(match.groups()) > 2 else line
                        })
                        break
                if not any(ing["item"] == line for ing in ingredients) and len(line) > 3:
                    ingredients.append({"quantity": "1", "unit": "", "item": line})
        
        # Limit ingredients
        ingredients = ingredients[:15]
        
        # Try to extract instructions
        instructions = []
        for line in lines:
            line = line.strip()
            if any(marker in line for marker in ['Step', '1.', '2.', '3.', '4.', '5.']) or len(line) > 50:
                if not line in instructions:
                    instructions.append(line)
        
        instructions = instructions[:10]
        if not instructions:
            instructions = ["Recipe instructions not available. Please visit the source website."]
        
        result = {
            "title": title,
            "cuisine": "Unknown",
            "prep_time": "10 mins",
            "cook_time": "20 mins",
            "total_time": "30 mins",
            "servings": 4,
            "difficulty": "medium",
            "ingredients": ingredients if ingredients else [{"quantity": "1", "unit": "", "item": "See source website for ingredients"}],
            "instructions": instructions,
            "nutrition_estimate": {
                "calories": 300,
                "protein": "15g",
                "carbs": "30g",
                "fat": "12g"
            },
            "substitutions": ["No substitutions available without AI processing"],
            "shopping_list": {"Pantry": ["See source website for details"]},
            "related_recipes": ["Try other recipes from the same website"]
        }
        
        return {
            "success": True,
            "data": result,
            "note": "Extracted using fallback method (AI unavailable)"
        }


llm_service = LLMService()
