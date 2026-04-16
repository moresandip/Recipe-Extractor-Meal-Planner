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
      const result = await extractRecipe(url);
      setRecipe(result);
      onRecipeExtracted();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to extract recipe. Please check the URL and try again.');
    } finally {
      setLoading(false);
    }
  };

  const getDifficultyBadge = (difficulty) => {
    const badges = {
      easy: 'badge-easy',
      medium: 'badge-medium',
      hard: 'badge-hard'
    };
    return badges[difficulty?.toLowerCase()] || 'badge-easy';
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
              placeholder="https://www.allrecipes.com/recipe/..."
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
          <p style={{ color: '#dc2626', fontSize: '0.875rem' }}>{error}</p>
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
