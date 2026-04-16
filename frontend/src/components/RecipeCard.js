import React from 'react';
import { Clock, Users, BarChart3, ArrowRightLeft, ShoppingCart, Lightbulb, Utensils, CheckCircle2 } from 'lucide-react';

const RecipeCard = ({ recipe }) => {
  const getDifficultyBadge = (difficulty) => {
    const badges = {
      easy: { bg: '#d1fae5', color: '#065f46' },
      medium: { bg: '#fef3c7', color: '#92400e' },
      hard: { bg: '#fee2e2', color: '#991b1b' }
    };
    const badge = badges[difficulty?.toLowerCase()] || badges.easy;
    return badge;
  };

  const badge = getDifficultyBadge(recipe.difficulty);

  return (
    <div>
      {/* Header Card */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ flex: 1 }}>
            <span style={{
              display: 'inline-block',
              background: badge.bg,
              color: badge.color,
              padding: '0.25rem 0.75rem',
              borderRadius: '9999px',
              fontSize: '0.75rem',
              fontWeight: 600,
              textTransform: 'uppercase',
              marginBottom: '0.75rem'
            }}>
              {recipe.difficulty || 'Easy'}
            </span>
            
            <h1 style={{
              fontSize: '1.875rem',
              fontWeight: 700,
              color: '#1f2937',
              marginBottom: '0.5rem'
            }}>
              {recipe.title}
            </h1>
            
            <p style={{
              color: '#6b7280',
              fontSize: '0.875rem'
            }}>
              {recipe.cuisine} Cuisine
            </p>
          </div>

          <div style={{
            display: 'flex',
            gap: '1.5rem',
            flexWrap: 'wrap'
          }}>
            {recipe.prep_time && (
              <div style={{ textAlign: 'center' }}>
                <Clock size={20} color="#667eea" style={{ margin: '0 auto 0.25rem' }} />
                <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>Prep</p>
                <p style={{ fontSize: '0.875rem', fontWeight: 600, color: '#1f2937' }}>{recipe.prep_time}</p>
              </div>
            )}
            {recipe.cook_time && (
              <div style={{ textAlign: 'center' }}>
                <Clock size={20} color="#667eea" style={{ margin: '0 auto 0.25rem' }} />
                <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>Cook</p>
                <p style={{ fontSize: '0.875rem', fontWeight: 600, color: '#1f2937' }}>{recipe.cook_time}</p>
              </div>
            )}
            {recipe.servings && (
              <div style={{ textAlign: 'center' }}>
                <Users size={20} color="#667eea" style={{ margin: '0 auto 0.25rem' }} />
                <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>Servings</p>
                <p style={{ fontSize: '0.875rem', fontWeight: 600, color: '#1f2937' }}>{recipe.servings}</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '1.5rem'
      }}>
        {/* Ingredients */}
        <div className="card">
          <h3 style={{
            fontSize: '1.125rem',
            fontWeight: 600,
            color: '#1f2937',
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <ShoppingCart size={20} color="#667eea" />
            Ingredients
          </h3>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {recipe.ingredients?.map((ingredient, idx) => (
              <li key={idx} style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                fontSize: '0.875rem',
                color: '#374151'
              }}>
                <CheckCircle2 size={16} color="#10b981" />
                <span style={{ fontWeight: 600 }}>{ingredient.quantity} {ingredient.unit}</span>
                <span>{ingredient.item}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Instructions */}
        <div className="card" style={{ gridColumn: 'span 2' }}>
          <h3 style={{
            fontSize: '1.125rem',
            fontWeight: 600,
            color: '#1f2937',
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <Utensils size={20} color="#667eea" />
            Instructions
          </h3>
          <ol style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {recipe.instructions?.map((step, idx) => (
              <li key={idx} style={{
                display: 'flex',
                gap: '0.75rem',
                fontSize: '0.875rem',
                color: '#374151',
                lineHeight: 1.6
              }}>
                <span style={{
                  flexShrink: 0,
                  width: '28px',
                  height: '28px',
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.875rem',
                  fontWeight: 600
                }}>
                  {idx + 1}
                </span>
                <span style={{ paddingTop: '0.25rem' }}>{step}</span>
              </li>
            ))}
          </ol>
        </div>

        {/* Nutrition */}
        {recipe.nutrition_estimate && (
          <div className="card">
            <h3 style={{
              fontSize: '1.125rem',
              fontWeight: 600,
              color: '#1f2937',
              marginBottom: '1rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              <BarChart3 size={20} color="#667eea" />
              Nutrition (per serving)
            </h3>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(2, 1fr)',
              gap: '0.75rem'
            }}>
              {recipe.nutrition_estimate.calories && (
                <div style={{
                  background: '#f3f4f6',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  textAlign: 'center'
                }}>
                  <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>Calories</p>
                  <p style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1f2937' }}>
                    {recipe.nutrition_estimate.calories}
                  </p>
                </div>
              )}
              {recipe.nutrition_estimate.protein && (
                <div style={{
                  background: '#f3f4f6',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  textAlign: 'center'
                }}>
                  <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>Protein</p>
                  <p style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1f2937' }}>
                    {recipe.nutrition_estimate.protein}
                  </p>
                </div>
              )}
              {recipe.nutrition_estimate.carbs && (
                <div style={{
                  background: '#f3f4f6',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  textAlign: 'center'
                }}>
                  <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>Carbs</p>
                  <p style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1f2937' }}>
                    {recipe.nutrition_estimate.carbs}
                  </p>
                </div>
              )}
              {recipe.nutrition_estimate.fat && (
                <div style={{
                  background: '#f3f4f6',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  textAlign: 'center'
                }}>
                  <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>Fat</p>
                  <p style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1f2937' }}>
                    {recipe.nutrition_estimate.fat}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Substitutions */}
        {recipe.substitutions && recipe.substitutions.length > 0 && (
          <div className="card">
            <h3 style={{
              fontSize: '1.125rem',
              fontWeight: 600,
              color: '#1f2937',
              marginBottom: '1rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              <ArrowRightLeft size={20} color="#667eea" />
              Substitutions
            </h3>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {recipe.substitutions.map((sub, idx) => (
                <li key={idx} style={{
                  fontSize: '0.875rem',
                  color: '#374151',
                  background: '#f0fdf4',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  borderLeft: '3px solid #22c55e'
                }}>
                  {sub}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Shopping List */}
        {recipe.shopping_list && Object.keys(recipe.shopping_list).length > 0 && (
          <div className="card" style={{ gridColumn: 'span 2' }}>
            <h3 style={{
              fontSize: '1.125rem',
              fontWeight: 600,
              color: '#1f2937',
              marginBottom: '1rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              <ShoppingCart size={20} color="#667eea" />
              Shopping List
            </h3>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
              gap: '1rem'
            }}>
              {Object.entries(recipe.shopping_list).map(([category, items]) => (
                <div key={category} style={{
                  background: '#f9fafb',
                  padding: '1rem',
                  borderRadius: '8px'
                }}>
                  <h4 style={{
                    fontSize: '0.875rem',
                    fontWeight: 600,
                    color: '#667eea',
                    textTransform: 'capitalize',
                    marginBottom: '0.5rem'
                  }}>
                    {category}
                  </h4>
                  <ul style={{ listStyle: 'none' }}>
                    {items.map((item, idx) => (
                      <li key={idx} style={{
                        fontSize: '0.875rem',
                        color: '#374151',
                        padding: '0.25rem 0'
                      }}>
                        • {item}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Related Recipes */}
        {recipe.related_recipes && recipe.related_recipes.length > 0 && (
          <div className="card" style={{ gridColumn: 'span 2' }}>
            <h3 style={{
              fontSize: '1.125rem',
              fontWeight: 600,
              color: '#1f2937',
              marginBottom: '1rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              <Lightbulb size={20} color="#667eea" />
              Related Recipes
            </h3>
            <div style={{
              display: 'flex',
              gap: '0.75rem',
              flexWrap: 'wrap'
            }}>
              {recipe.related_recipes.map((related, idx) => (
                <span key={idx} style={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  padding: '0.5rem 1rem',
                  borderRadius: '9999px',
                  fontSize: '0.875rem',
                  fontWeight: 500
                }}>
                  {related}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecipeCard;
