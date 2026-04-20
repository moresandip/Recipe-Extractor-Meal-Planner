import axios from 'axios';

const API_BASE_URL = (process.env.REACT_APP_API_URL || 'http://localhost:8080') + '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000,
});

// Add error interceptor for clearer diagnostic messages
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.log('API Error:', error);
    
    if (!error.response) {
      // Network error or backend down
      console.error('Network Error: Backend might be down or unreachable');
      error.message = '❌ CANNOT CONNECT TO BACKEND!\n\nBackend server is not running on port 8080.\n\nFIX:\n1. Open new CMD\n2. cd backend\n3. venv\\Scripts\\python -m uvicorn app.main:app --host 0.0.0.0 --port 8080';
    } else if (error.response.status === 404) {
      const errorDetail = error.response?.data?.detail || 'Not Found';
      console.error('404 Error:', errorDetail);
      
      // Check if it's a website 404 or API 404
      if (errorDetail.includes('recipe') || errorDetail.includes('Unable to fetch')) {
        error.message = `❌ ${errorDetail}\n\nWebsite is blocking the scraper.\n\nTry these URLs instead:\n- https://www.simplyrecipes.com/\n- https://www.bonappetit.com/\n- https://www.foodnetwork.com/`;
      } else {
        error.message = `❌ API Error: ${errorDetail}\n\nBackend endpoint not found. Restart backend server.`;
      }
    } else if (error.response.status === 400) {
      const errorDetail = error.response?.data?.detail || 'Bad Request';
      error.message = `❌ ${errorDetail}`;
    }
    
    return Promise.reject(error);
  }
);

// Extract recipe from URL
export const extractRecipe = async (url) => {
  const response = await api.post('/extract', { url });
  return response.data;
};

// Get all saved recipes
export const getRecipes = async (skip = 0, limit = 100) => {
  const response = await api.get('/recipes', {
    params: { skip, limit }
  });
  return response.data;
};

// Get single recipe by ID
export const getRecipe = async (id) => {
  const response = await api.get(`/recipes/${id}`);
  return response.data;
};

// Delete recipe
export const deleteRecipe = async (id) => {
  const response = await api.delete(`/recipes/${id}`);
  return response.data;
};

// Generate meal plan
export const generateMealPlan = async (recipeIds) => {
  const response = await api.post('/meal-plan', { recipe_ids: recipeIds });
  return response.data;
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

// Demo extract - returns sample recipe for testing
export const demoExtract = async () => {
  const response = await api.post('/demo-extract');
  return response.data;
};

export default api;
