# Recipe Extractor & Meal Planner

A full-stack application that extracts structured recipe data from any recipe blog URL using AI (Google Gemini via LangChain), stores it in PostgreSQL, and provides a beautiful React frontend for viewing and managing recipes.

![Tech Stack](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green?style=flat-square&logo=fastapi)
![React](https://img.shields.io/badge/React-18+-blue?style=flat-square&logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue?style=flat-square&logo=postgresql)

---

## Features

### TAB 1 - Extract Recipe
- **URL Input**: Paste any recipe blog URL
- **Web Scraping**: Uses BeautifulSoup to extract page content
- **AI Processing**: Google Gemini LLM extracts structured data:
  - Recipe title, cuisine, prep/cook/total time
  - Difficulty level (easy/medium/hard)
  - Ingredients with quantity/unit/item separation
  - Step-by-step instructions
  - Nutritional estimates (calories, protein, carbs, fat)
  - 3 ingredient substitutions with reasoning
  - Categorized shopping list (dairy, produce, pantry, etc.)
  - 3 related recipe suggestions

### TAB 2 - Saved Recipes (History)
- **Table View**: List all extracted recipes with metadata
- **Details Modal**: View full recipe in structured layout
- **Delete**: Remove recipes from database

### Bonus Features
- Meal planning mode (combine 3-7 recipes)
- Categorized shopping lists
- Clean, minimal UI with responsive design

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.11+, FastAPI |
| Database | PostgreSQL 14+ |
| ORM | SQLAlchemy |
| AI/LLM | Google Gemini via LangChain |
| Web Scraping | BeautifulSoup4, requests |
| Frontend | React 18+, Lucide Icons |
| Styling | CSS3 with custom design system |

---

## Prerequisites

- Python 3.11 or higher
- Node.js 18+ and npm/yarn
- PostgreSQL 14+ (local or cloud)
- Google Gemini API Key (free tier available)

---

## Setup Instructions

### 1. Clone and Navigate

```bash
cd "Recipe Extractor & Meal Planner"
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL and Gemini API key
```

### 3. Environment Variables

Edit `backend/.env`:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/recipe_extractor

# Gemini API Key (Get from https://ai.google.dev/)
GEMINI_API_KEY=your_gemini_api_key_here

# App Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=true
```

### 4. Database Setup

```bash
# Create PostgreSQL database
createdb recipe_extractor

# Tables are auto-created on first run
```

### 5. Start Backend

```bash
python run.py
```

Backend runs at: `http://localhost:8000`

API docs at: `http://localhost:8000/docs`

### 6. Frontend Setup

```bash
# In a new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs at: `http://localhost:3000`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/extract` | Extract recipe from URL |
| GET | `/api/recipes` | List all saved recipes |
| GET | `/api/recipes/{id}` | Get specific recipe |
| DELETE | `/api/recipes/{id}` | Delete recipe |
| POST | `/api/meal-plan` | Generate meal plan from recipe IDs |
| GET | `/api/health` | Health check |

### Example API Request

```bash
curl -X POST "http://localhost:8000/api/extract" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/"}'
```

---

## Project Structure

```
Recipe Extractor & Meal Planner/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py          # FastAPI endpoints
│   │   │   └── schemas.py         # Pydantic models
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py          # Settings management
│   │   │   └── database.py        # SQLAlchemy setup
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── recipe.py          # Database model
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── scraper.py         # BeautifulSoup scraper
│   │   │   └── llm_service.py     # Gemini LangChain integration
│   │   ├── utils/
│   │   │   └── __init__.py
│   │   └── main.py                # FastAPI application
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py                     # Entry point
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── RecipeExtractor.js
│   │   │   ├── RecipeHistory.js
│   │   │   ├── RecipeCard.js
│   │   │   └── RecipeModal.js
│   │   ├── services/
│   │   │   └── api.js             # API client
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
├── prompts/                       # LangChain prompts
│   ├── recipe_extraction.md
│   ├── nutrition_estimation.md
│   ├── substitution_generation.md
│   ├── shopping_list_generation.md
│   ├── related_recipes.md
│   └── meal_planning.md
├── sample_data/                   # Test data
│   ├── example_urls.txt
│   ├── sample_output_1.json
│   ├── sample_output_2.json
│   └── sample_output_3.json
└── README.md
```

---

## LangChain Prompts

All prompts used for LLM processing are documented in the `prompts/` folder:

1. **recipe_extraction.md** - Main extraction prompt
2. **nutrition_estimation.md** - Calorie/macro calculation
3. **substitution_generation.md** - Dietary alternatives
4. **shopping_list_generation.md** - Grocery categorization
5. **related_recipes.md** - Pairing suggestions
6. **meal_planning.md** - Weekly meal planning

---

## Testing

### Test URLs

Sample URLs for testing are in `sample_data/example_urls.txt`:
- AllRecipes (grilled cheese, cookies, pasta)
- Food Network (carbonara, tacos)
- Serious Eats (pancakes, burgers)
- Bon Appetit (roasted chicken)
- Minimalist Baker (vegan recipes)

### Run Backend Tests

```bash
cd backend
pytest
```

### Manual Testing Checklist

1. Extract recipe from URL ✓
2. View structured output ✓
3. Check history table ✓
4. Open details modal ✓
5. Delete recipe ✓
6. Verify database persistence ✓

---

## Screenshots

The application includes:
- Clean gradient header with tab navigation
- URL input with extract button
- Card-based recipe display
- Structured ingredient lists
- Numbered instructions
- Nutrition grid
- Categorized shopping list
- History table with actions
- Modal for recipe details

---

## Common Issues & Solutions

### Issue: CORS errors in frontend
**Solution**: Backend has CORS enabled. Check `app/main.py` CORS middleware config.

### Issue: Gemini API errors
**Solution**: Verify `GEMINI_API_KEY` in `.env` file. Get key from https://ai.google.dev/

### Issue: Database connection failed
**Solution**: Check `DATABASE_URL` format:
```
postgresql://user:password@host:port/database
```

### Issue: URL scraping timeout
**Solution**: Some sites block scrapers. Try different URLs or add delays in `scraper.py`.

---

## Deployment

### Backend (Render/Railway/Heroku)

1. Set environment variables
2. Configure PostgreSQL database
3. Deploy with `pip install -r requirements.txt && python run.py`

### Frontend (Vercel/Netlify)

1. Set `REACT_APP_API_URL` to backend URL
2. Build: `npm run build`
3. Deploy build folder

### Docker (Optional)

```dockerfile
# Dockerfile for backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

---

## Performance Notes

- LLM processing takes 5-15 seconds per recipe
- Frontend has 60-second timeout for extraction requests
- Database stores limited HTML (50KB max) to save space
- Consider caching for repeated URLs

---

## License

MIT License - Free for personal and commercial use.

---

## Author

Recipe Extractor & Meal Planner - Built with FastAPI, React, and Google Gemini AI.

For questions or issues, please check the sample data and prompts folders for examples.
#   R e c i p e - E x t r a c t o r - M e a l - P l a n n e r  
 #   R e c i p e - E x t r a c t o r - M e a l - P l a n n e r  
 