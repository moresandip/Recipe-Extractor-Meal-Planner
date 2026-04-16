# Shopping List Generation Prompt

## Purpose
Organize recipe ingredients into categorized shopping lists for easier grocery shopping.

## Prompt Template

```
You are a shopping list organizer. Group the following recipe ingredients into grocery store categories.

RECIPE: {recipe_title}
INGREDIENTS:
{ingredients_list}

Group items into these standard categories:
- produce (fruits, vegetables, fresh herbs)
- dairy (milk, cheese, butter, yogurt, eggs)
- meat (chicken, beef, pork, fish)
- pantry (flour, sugar, oil, spices, canned goods, pasta, rice)
- bakery (bread, tortillas, buns)
- frozen (frozen vegetables, ice cream)
- beverages
- other

Return in JSON format:
{
    "category_name": ["item1", "item2", ...],
    ...
}

Rules:
- Only include categories that have items
- Use lowercase for category names
- List items as they appear in the recipe (cleaned up)
- Combine similar items if possible
```

## Standard Grocery Categories

| Category | Examples |
|----------|----------|
| produce | tomatoes, onions, garlic, lettuce, apples |
| dairy | milk, cheddar cheese, butter, heavy cream |
| meat | chicken breast, ground beef, salmon |
| pantry | olive oil, flour, sugar, salt, pasta |
| bakery | bread, burger buns, tortillas |
| frozen | frozen peas, pizza dough |
| beverages | wine, stock, broth |

## Output Format
JSON object with category names as keys and arrays of items as values.
