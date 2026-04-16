# Recipe Extraction Prompt

## Purpose
Extract structured recipe data from scraped HTML content using a Large Language Model.

## Prompt Template

```
You are a recipe extraction assistant. Extract structured recipe data from the following content.

PAGE CONTENT:
{scraped_content}

STRUCTURED DATA (JSON-LD if available):
{structured_data}

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
- Difficulty should be based on: 
  * easy (beginner-friendly, <30 min)
  * medium (moderate skills, 30-60 min)
  * hard (complex techniques, >60 min)
- For nutrition estimates, calculate based on standard serving sizes
```

## Example Usage (Python/LangChain)

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key="YOUR_API_KEY",
    temperature=0.3
)

prompt = ChatPromptTemplate.from_template(RECIPE_EXTRACTION_PROMPT)
chain = prompt | llm

result = chain.invoke({
    "scraped_content": page_text,
    "structured_data": json_ld_data
})
```

## Output Format
JSON with all extracted recipe information structured for storage and display.
