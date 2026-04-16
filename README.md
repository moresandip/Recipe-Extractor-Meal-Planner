# 🍽️ Recipe Extractor & Meal Planner

A full-stack, AI-powered application that seamlessly extracts structured recipe data from any culinary blog URL. Using **Google Gemini** (via LangChain), this tool parses messy web pages into clean, structured data, stores it in PostgreSQL, and serves it through a beautiful modern React frontend interface.

![Tech Stack](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green?style=flat-square&logo=fastapi)
![React](https://img.shields.io/badge/React-18+-blue?style=flat-square&logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue?style=flat-square&logo=postgresql)

---

## 📑 Table of Contents
1. [Features](#-features)
2. [Tech Stack](#-tech-stack)
3. [Prerequisites](#-prerequisites)
4. [Quick Start Setup](#-quick-start-setup)
5. [API Endpoints](#-api-endpoints)
6. [Project Structure](#-project-structure)
7. [LangChain Prompts](#-langchain-prompts)
8. [Testing & Usage](#-testing--usage)
9. [Common Issues & Solutions](#-common-issues--solutions)
10. [Deployment](#-deployment)

---

## ✨ Features

### 🔍 TAB 1: Extract Recipe
- **URL Input**: Paste any messy recipe blog URL and let the AI do the heavy lifting.
- **Web Scraping**: Built-in BeautifulSoup extraction to grab unstructured page content.
- **Deep AI Processing (Google Gemini & LangChain)**:
  - 🕒 Prep, cook, and total times.
  - 📊 Difficulty level (Easy/Medium/Hard).
  - 🥬 Precision Ingredients (Separates quantity, unit, and item name seamlessly).
  - 📜 Step-by-step instructions.
  - 🥗 Nutritional estimations (Calories, Protein, Carbs, Fat).
  - 🔄 Smart ingredient substitutions with explanations.
  - 🛒 Categorized shopping lists (Dairy, Produce, Pantry, etc.).
  - 🔗 Related recipe suggestions.

### 📚 TAB 2: Saved Recipes (History)
- **Table View**: Browse your entire extracted recipe database.
- **Details Modal**: A distraction-free popup featuring the completely parsed recipe.
- **Manage**: Delete recipes with a single click.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----------|------------|
| **Backend** | Python 3.11+, FastAPI |
| **Database** | PostgreSQL 14+ |
| **ORM** | SQLAlchemy |
| **AI / LLM Core** | Google Gemini via LangChain |
| **Web Scraping** | BeautifulSoup4, Requests |
| **Frontend UI** | React 18+, Lucide Icons |
| **Styling** | Vanilla CSS3 (Custom Design System) |

---

## 📋 Prerequisites

Make sure you have the following installed to run this project smoothly:
- **Python 3.11+**
- **Node.js 18+** (with npm or yarn)
- **PostgreSQL 14+** (running locally or via the cloud)
- **Google Gemini API Key** (Fetch yours for free from [Google AI Studio](https://ai.google.dev/))

---

## 🚀 Quick Start Setup

For the fastest setup, ensure your requirements are met and run the provided Windows batch files! 

If you prefer to set it up manually:

### 1. Backend Setup

```bash
cd "Recipe Extractor & Meal Planner"/backend

# 1. Create & Activate your virtual environment
python -m venv venv
venv\Scripts\activate   # Mac/Linux: source venv/bin/activate

# 2. Install Python packages
pip install -r requirements.txt

# 3. Create your environment file
cp .env.example .env
```
Edit the `.env` to include your Database URL and your `GEMINI_API_KEY`.

### 2. Frontend Setup

```bash
cd frontend

# 1. Install Node dependencies
npm install

# 2. Start the development server
npm start
```
The React frontend should now be running at [http://localhost:3000](http://localhost:3000).

---

## 🔌 API Endpoints

The backend is fully documented via Swagger UI. Once running, you can visit `http://localhost:8000/docs` to test endpoints.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/extract` | Extract a completely new recipe from a provided URL |
| `GET` | `/api/recipes` | Fetch the list of all saved recipes |
| `GET` | `/api/recipes/{id}` | Read a specific recipe by ID |
| `DELETE` | `/api/recipes/{id}` | Permanently delete a recipe |
| `POST` | `/api/meal-plan` | Generate a meal plan automatically from recipe IDs |
| `GET` | `/api/health` | Service health status check |

---

## 🏗️ Project Structure

The repository is modularly split between the frontend and the AI-focused backend.

```text
Recipe Extractor & Meal Planner
├── backend/                  # FastAPI & AI Engine
│   ├── app/                  # Application Logic (API, Core, DB Models)
│   ├── .env.example          # Template environment config
│   └── run.py                # Backend execution entry point
├── frontend/                 # React UI Application
│   ├── public/               # Static assets
│   ├── src/                  # React Components, Services, and CSS
│   └── package.json          # Node dependencies
├── prompts/                  # LangChain System Prompts (Crucial for AI Extraction)
├── sample_data/              # Test URL lists and JSON examples
└── start_servers.bat         # Windows quick-execution script
```

All LangChain Prompts used for AI generation exist in `/prompts`, split modularly by task (extraction, nutrition, shopping list execution, etc).

---

## 🧪 Testing & Usage

You can test extraction immediately using our sample list of URLs located in `sample_data/example_urls.txt`.
Supported structures include pages from *AllRecipes*, *Food Network*, *Serious Eats*, *Bon Appetit*, and basically any standardized food blog.

### Automation Testing
To test the backend core functions:
```bash
cd backend
pytest
```

---

## 🩹 Common Issues & Solutions

- **`MODULE_NOT_FOUND` on Windows**: Having an ampersand (`&`) in the project folder name disrupts `react-scripts`. Our `package.json` resolves this natively, but if problems persist, rename the repository folder to just `RecipeExtractor`.
- **CORS Errors**: Check your `app/main.py` CORS middleware if your frontend is attempting to fetch from an irregular port.
- **Gemini Quota Exceeded**: Make sure your Google AI Studio account has billing enabled (or isn't heavily rate-limited for free-tier users).
- **Timeouts**: Due to complex LLM context window scraping, extraction can take between 5 - 15 seconds. Ensure you do not refresh the page during this process.

---

## 🌍 Deployment

**Backend**:
Can be easily deployed on services like Render, Heroku, or PythonAnywhere. Ensure the `DATABASE_URL` is set to point toward your production Postgres database.

**Frontend**:
Standard `npx react-scripts build` architecture. Ideal for one-click deployments to Vercel or Netlify. When deploying frontend, set `REACT_APP_API_URL` locally as your hosted backend URL.

---

## 📜 License & Credit

MIT License - Free for personal and commercial use.

Enjoy hassle-free recipe hunting! 🥙