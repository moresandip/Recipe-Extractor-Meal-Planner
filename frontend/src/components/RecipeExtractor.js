import React, { useState } from 'react';
import { Loader2, Link2, ChefHat } from 'lucide-react';
import { extractRecipe } from '../services/api';
import RecipeCard from './RecipeCard';

const RecipeExtractor = ({ onRecipeExtracted }) => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [recipe, setRecipe] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url.trim()) return;

    setLoading(true);
    setError(null);
    setRecipe(null);

    try {
      const response = await extractRecipe(url);
      setRecipe(response.data);
      setError('');
      
      // Check if using fallback extraction
      if (response.data && response.data.note && response.data.note.includes('fallback')) {
        setError('⚠️ AI extraction unavailable. Using basic extraction. For better results, check Gemini API key in backend/.env');
      }
      onRecipeExtracted();
    } catch (err) {
      let errorMessage = err.response?.data?.detail || err.message || 'Failed to extract recipe. Please check the URL and try again.';
      
      // Log full error for debugging
      console.log('Full error:', err);
      console.log('Error response:', err.response);
      
      // Add helpful troubleshooting tips based on error type
      if (!err.response) {
        errorMessage = `❌ CANNOT CONNECT TO BACKEND!\n\nBackend server is not running on port 8080.\n\n🔧 EASY FIX:\nDouble-click: START-EVERYTHING.bat\n(This starts both backend + frontend)\n\n🔧 MANUAL FIX:\n1. Open CMD\n2. cd backend\n3. venv\\Scripts\\python -m uvicorn app.main:app --host 0.0.0.0 --port 8080\n\n4. Refresh this page`;
      } else if (err.response.status === 404) {
        if (errorMessage.includes('Unable to fetch') || errorMessage.includes('recipe')) {
          errorMessage = `❌ WEBSITE BLOCKING SCRAPER!\n\n${errorMessage}\n\n🔧 TRY THESE WORKING URLS:\n• https://www.simplyrecipes.com/recipes/grilled_cheese/\n• https://www.bonappetit.com/recipe/basically-grilled-cheese\n• https://www.foodnetwork.com/recipes/grilled-cheese\n\nAllRecipes blocks scrapers. Use other sites.`;
        } else {
          errorMessage = `❌ API ENDPOINT NOT FOUND!\n\nBackend API is not responding correctly.\n\n🔧 FIX: Restart backend server`;
        }
      } else if (err.response.status === 400) {
        errorMessage = `❌ ${errorMessage}\n\nWebsite is blocking the scraper. Try a different recipe URL.`;
      } else if (err.response.status === 500) {
        if (errorMessage.includes('API key') || errorMessage.includes('Gemini') || errorMessage.includes('model')) {
          errorMessage = `❌ GEMINI API KEY ERROR!\n\n${errorMessage}\n\n🔧 FIX:\n1. Check if GEMINI_API_KEY in backend/.env is valid\n2. Get new API key from: https://makersuite.google.com/app/apikey\n3. Update key in backend/.env file\n4. Restart backend server`;
        } else if (errorMessage.includes('API key') || errorMessage.includes('Gemini') || errorMessage.includes('model')) {
          errorMessage = `❌ GEMINI API KEY ERROR!\n\n${errorMessage}\n\n🔧 FIX:\n1. Check if GEMINI_API_KEY in backend/.env is valid\n2. Get new API key from: https://makersuite.google.com/app/apikey\n3. Update key in backend/.env file\n4. Restart backend server`;
        } else {
          errorMessage = `❌ SERVER ERROR!\n\n${errorMessage}\n\n🔧 Backend may need restart.`;
        }
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Input Section */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h2 style={{
          fontSize: '1.25rem',
          fontWeight: 600,
          color: '#1f2937',
          marginBottom: '1rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
          <Link2 size={20} color="#667eea" />
          Enter Recipe URL
        </h2>
        
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://www.simplyrecipes.com/... (AllRecipes blocks scrapers)"
              className="input"
              style={{ flex: 1, minWidth: '250px' }}
              required
            />
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || !url.trim()}
            >
              {loading ? (
                <>
                  <Loader2 size={18} className="spin" />
                  Extracting...
                </>
              ) : (
                <>
                  <ChefHat size={18} />
                  Extract Recipe
                </>
              )}
            </button>
          </div>
        </form>

        <p style={{
          fontSize: '0.875rem',
          color: '#6b7280',
          marginTop: '0.75rem'
        }}>
          Example: https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="card" style={{ 
          background: '#fef2f2', 
          border: '1px solid #fecaca',
          marginBottom: '1.5rem'
        }}>
          <p style={{ color: '#dc2626', fontSize: '0.875rem', whiteSpace: 'pre-line' }}>{error}</p>
        </div>
      )}

      {/* Recipe Result */}
      {recipe && (
        <div className="fade-in">
          <RecipeCard recipe={recipe} />
        </div>
      )}
    </div>
  );
};

export default RecipeExtractor;
