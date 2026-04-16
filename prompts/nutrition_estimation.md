# Nutrition Estimation Prompt

## Purpose
Generate approximate nutritional information for a recipe based on its ingredients and quantities.

## Prompt Template

```
You are a nutrition estimation assistant. Calculate approximate nutritional values per serving for the following recipe.

RECIPE: {recipe_title}
INGREDIENTS:
{ingredients_list}
SERVINGS: {servings}

Calculate the following per serving:
1. Calories (kcal)
2. Protein (grams with 'g' suffix)
3. Carbohydrates (grams with 'g' suffix)
4. Fat (grams with 'g' suffix)

Use standard nutritional values:
- 1g protein = 4 calories
- 1g carbs = 4 calories  
- 1g fat = 9 calories
- Account for cooking methods (frying adds fat, baking is moderate, grilling is lower)

Return in JSON format:
{
    "calories": <number>,
    "protein": "<value>g",
    "carbs": "<value>g",
    "fat": "<value>g",
    "calculation_notes": "brief explanation of estimation method"
}

Be reasonable in estimates - typical home-cooked meals range 300-800 calories per serving.
```

## Example Usage

```python
nutrition_prompt = """
Calculate nutrition for:
Title: {title}
Ingredients: {ingredients}
Servings: {servings}
"""

result = llm.invoke(nutrition_prompt.format(
    title=recipe.title,
    ingredients=formatted_ingredients,
    servings=recipe.servings
))
```

## Notes
- Estimates are approximate and for informational purposes
- Actual values may vary based on specific brands and preparation methods
