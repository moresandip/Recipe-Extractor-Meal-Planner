import React, { useState, useEffect } from 'react';
import { Clock, Trash2, Eye, Loader2, AlertCircle, UtensilsCrossed } from 'lucide-react';
import { getRecipes, deleteRecipe } from '../services/api';
import RecipeModal from './RecipeModal';

const RecipeHistory = () => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(null);

  useEffect(() => {
    fetchRecipes();
  }, []);

  const fetchRecipes = async () => {
    try {
      setLoading(true);
      const data = await getRecipes();
      setRecipes(data);
      setError(null);
    } catch (err) {
      setError('Failed to load recipes. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this recipe?')) return;

    setDeleteLoading(id);
    try {
      await deleteRecipe(id);
      setRecipes(recipes.filter(r => r.id !== id));
    } catch (err) {
      alert('Failed to delete recipe');
    } finally {
      setDeleteLoading(null);
    }
  };

  const getDifficultyBadge = (difficulty) => {
    const badges = {
      easy: { bg: '#d1fae5', color: '#065f46', label: 'Easy' },
      medium: { bg: '#fef3c7', color: '#92400e', label: 'Medium' },
      hard: { bg: '#fee2e2', color: '#991b1b', label: 'Hard' }
    };
    const badge = badges[difficulty?.toLowerCase()] || badges.easy;
    return badge;
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
        <Loader2 size={40} color="#667eea" className="spin" style={{ margin: '0 auto 1rem' }} />
        <p style={{ color: '#6b7280' }}>Loading recipes...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card" style={{ 
        background: '#fef2f2', 
        border: '1px solid #fecaca',
        textAlign: 'center',
        padding: '2rem'
      }}>
        <AlertCircle size={40} color="#dc2626" style={{ margin: '0 auto 1rem' }} />
        <p style={{ color: '#dc2626' }}>{error}</p>
        <button
          onClick={fetchRecipes}
          className="btn btn-primary"
          style={{ marginTop: '1rem' }}
        >
          Try Again
        </button>
      </div>
    );
  }

  if (recipes.length === 0) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
        <UtensilsCrossed size={48} color="#d1d5db" style={{ margin: '0 auto 1rem' }} />
        <h3 style={{ color: '#374151', marginBottom: '0.5rem' }}>No recipes yet</h3>
        <p style={{ color: '#6b7280', marginBottom: '1.5rem' }}>
          Extract your first recipe to see it here
        </p>
      </div>
    );
  }

  return (
    <div>
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1rem'
        }}>
          <div>
            <h2 style={{
              fontSize: '1.25rem',
              fontWeight: 600,
              color: '#1f2937'
            }}>
              Saved Recipes
            </h2>
            <p style={{ color: '#6b7280', fontSize: '0.875rem', marginTop: '0.25rem' }}>
              {recipes.length} recipe{recipes.length !== 1 ? 's' : ''} extracted
            </p>
          </div>
          <button
            onClick={fetchRecipes}
            className="btn btn-secondary"
          >
            Refresh
          </button>
        </div>
      </div>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Recipe</th>
              <th>Cuisine</th>
              <th>Difficulty</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {recipes.map((recipe) => {
              const badge = getDifficultyBadge(recipe.difficulty);
              return (
                <tr key={recipe.id}>
                  <td>
                    <div style={{ fontWeight: 600, color: '#1f2937' }}>
                      {recipe.title}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '0.25rem' }}>
                      {recipe.url.substring(0, 50)}...
                    </div>
                  </td>
                  <td>{recipe.cuisine || 'Unknown'}</td>
                  <td>
                    <span style={{
                      background: badge.bg,
                      color: badge.color,
                      padding: '0.25rem 0.75rem',
                      borderRadius: '9999px',
                      fontSize: '0.75rem',
                      fontWeight: 600
                    }}>
                      {badge.label}
                    </span>
                  </td>
                  <td>{formatDate(recipe.created_at)}</td>
                  <td>
                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                      <button
                        onClick={() => setSelectedRecipe(recipe)}
                        className="btn btn-secondary"
                        style={{ padding: '0.5rem' }}
                        title="View Details"
                      >
                        <Eye size={18} />
                      </button>
                      <button
                        onClick={() => handleDelete(recipe.id)}
                        className="btn btn-danger"
                        style={{ padding: '0.5rem' }}
                        disabled={deleteLoading === recipe.id}
                        title="Delete"
                      >
                        {deleteLoading === recipe.id ? (
                          <Loader2 size={18} className="spin" />
                        ) : (
                          <Trash2 size={18} />
                        )}
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {selectedRecipe && (
        <RecipeModal
          recipe={selectedRecipe}
          onClose={() => setSelectedRecipe(null)}
        />
      )}
    </div>
  );
};

export default RecipeHistory;
