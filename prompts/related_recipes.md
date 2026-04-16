# Related Recipe Suggestions Prompt

## Purpose
Suggest complementary dishes that pair well with the extracted recipe.

## Prompt Template

```
You are a meal pairing expert. Suggest 3 recipes that would pair well with the following dish.

RECIPE: {recipe_title}
CUISINE: {cuisine}
MEAL TYPE: {meal_type} (appetizer, main, dessert, etc.)
KEY INGREDIENTS: {key_ingredients}

Consider:
- Complementary flavors (contrasting or matching)
- Traditional pairings for this cuisine
- Complete meal balance (appetizer + main + side + dessert)
- Seasonal appropriateness
- Texture contrast

Return as a JSON array of recipe names:
[
    "Related Recipe 1",
    "Related Recipe 2", 
    "Related Recipe 3"
]

Make suggestions specific and appealing, not generic (e.g., "Garlic Roasted Potatoes" not just "Potatoes").
```

## Pairing Logic

### If Main Dish:
- Suggest sides, appetizers, or desserts
- Balance heavy mains with light sides
- Match cuisine style

### If Side Dish:
- Suggest main proteins or other sides
- Think complete meal

### Common Pairings:
- Grilled Cheese → Tomato Soup, French Onion Soup
- Steak → Roasted Vegetables, Mashed Potatoes
- Pasta → Garlic Bread, Caesar Salad
- Curry → Naan, Rice, Raita
- Tacos → Guacamole, Mexican Rice, Margaritas

## Output Format
Array of 3 recipe name strings.
