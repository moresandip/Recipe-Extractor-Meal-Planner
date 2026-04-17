import axios from 'axios';

const API_BASE_URL = (process.env.REACT_APP_API_URL || 'http://localhost:8000') + '/api';

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
    if (!error.response) {
      // Network error or backend down
      console.error('Network Error: Backend might be down or unreachable');
      error.message = 'Cannot connect to backend server. Please ensure the backend is running on http://localhost:8000';
    } else if (error.response.status === 404) {
      console.error('404 Error: Route not found at ' + error.config.url);
      error.message = 'API endpoint not found. Please check backend configuration.';
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

export default api;
