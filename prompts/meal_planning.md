# Meal Planning Prompt

## Purpose
Generate a weekly meal plan and combined shopping list from multiple selected recipes.

## Prompt Template

```
You are a meal planning assistant. Create a balanced meal plan from the following recipes.

SELECTED RECIPES:
{recipes_json}

Generate:
1. A weekly meal schedule (Monday-Sunday)
2. A combined shopping list with merged quantities
3. Meal prep tips for efficiency
4. Total estimated prep + cook time

Return in JSON format:
{
    "meal_plan": {
        "monday": "Recipe Name",
        "tuesday": "Recipe Name",
        "wednesday": "Recipe Name",
        "thursday": "Recipe Name",
        "friday": "Recipe Name",
        "saturday": "Recipe Name",
        "sunday": "Recipe Name"
    },
    "combined_shopping_list": {
        "category_name": ["item with quantity"],
        ...
    },
    "prep_tips": [
        "Tip 1: batch prep vegetables",
        "Tip 2: cook grains in advance",
        ...
    ],
    "total_estimated_time": "X hours Y minutes",
    "nutrition_overview": {
        "avg_calories_per_day": "estimated range",
        "protein_focus_days": ["monday", "wednesday"],
        "vegetarian_days": ["tuesday"]
    }
}

Guidelines:
- Distribute recipes throughout the week
- Consider: variety, difficulty balance, prep time
- Merge similar ingredients (e.g., "2 onions + 3 onions" = "5 onions")
- Suggest lighter meals after heavier ones
- Include leftover utilization if applicable
```

## Meal Planning Tips

### Balance:
- Heavy meals (pasta, fried) → Light meals (salads, grilled)
- Long prep → Quick prep
- Variety in proteins and cuisines

### Shopping List Merging:
- Sum quantities of same items
- Convert to standard units
- Remove duplicates

### Prep Efficiency:
- Batch chop vegetables
- Pre-cook grains
- Marinate proteins in advance
- Prep sauces ahead

## Output Format
Complete meal plan JSON with schedule, shopping list, and tips.
