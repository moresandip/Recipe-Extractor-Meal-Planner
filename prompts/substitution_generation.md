# Ingredient Substitution Generation Prompt

## Purpose
Generate smart ingredient substitutions for dietary preferences, allergies, or availability.

## Prompt Template

```
You are a culinary substitution expert. Suggest 3 practical ingredient substitutions for the following recipe.

RECIPE: {recipe_title}
CUISINE: {cuisine}
DIFFICULTY: {difficulty}
INGREDIENTS:
{ingredients_list}

For each substitution:
1. Identify an ingredient that might need substitution (dietary restrictions, allergies, or common substitutions)
2. Suggest a replacement ingredient
3. Explain the reason/benefit

Return as a JSON array of strings:
[
    "Replace [ingredient] with [substitute] for [reason]",
    "Replace [ingredient] with [substitute] for [reason]",
    "Replace [ingredient] with [substitute] for [reason]"
]

Consider these categories:
- Dairy-free alternatives
- Gluten-free options
- Vegan substitutions
- Lower-calorie options
- Common pantry swaps
- Allergy-friendly alternatives

Make substitutions practical and maintain the dish's flavor profile.
```

## Example Substitutions by Category

### Dairy
- Butter → Olive oil, coconut oil, or vegan butter
- Milk → Almond milk, oat milk, or coconut milk
- Cheese → Nutritional yeast, cashew cheese
- Cream → Coconut cream, cashew cream

### Gluten
- All-purpose flour → Almond flour, rice flour, or gluten-free blend
- Breadcrumbs → Crushed nuts, oats, or gluten-free crackers

### Vegan
- Eggs → Flax eggs, applesauce, or aquafaba
- Honey → Maple syrup, agave nectar
- Meat → Tofu, tempeh, seitan, or mushrooms

## Output Format
Array of 3 substitution strings with reasoning.
