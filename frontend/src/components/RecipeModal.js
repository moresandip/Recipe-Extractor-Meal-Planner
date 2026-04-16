import React from 'react';
import { X, Clock, Users, BarChart3, ArrowRightLeft, ShoppingCart, Lightbulb, Utensils, CheckCircle2 } from 'lucide-react';
import RecipeCard from './RecipeCard';

const RecipeModal = ({ recipe, onClose }) => {
  // Prevent body scroll when modal is open
  React.useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#1f2937' }}>
            Recipe Details
          </h2>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              padding: '0.5rem',
              borderRadius: '8px',
              transition: 'background 0.2s'
            }}
            onMouseEnter={e => e.target.style.background = '#f3f4f6'}
            onMouseLeave={e => e.target.style.background = 'none'}
          >
            <X size={24} color="#6b7280" />
          </button>
        </div>
        
        <div className="modal-body">
          <RecipeCard recipe={recipe} />
        </div>
      </div>
    </div>
  );
};

export default RecipeModal;
