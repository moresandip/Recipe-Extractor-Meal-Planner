import React, { useState } from 'react';
import { ChefHat, History, Sparkles } from 'lucide-react';
import RecipeExtractor from './components/RecipeExtractor';
import RecipeHistory from './components/RecipeHistory';

function App() {
  const [activeTab, setActiveTab] = useState('extract');
  const [refreshHistory, setRefreshHistory] = useState(0);

  const handleRecipeExtracted = () => {
    setRefreshHistory(prev => prev + 1);
    setActiveTab('history');
  };

  return (
    <div style={{ minHeight: '100vh', padding: '2rem 1rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {/* Header */}
        <header style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ 
            display: 'inline-flex', 
            alignItems: 'center', 
            gap: '0.75rem',
            marginBottom: '0.5rem'
          }}>
            <div style={{
              background: 'white',
              padding: '0.75rem',
              borderRadius: '12px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
            }}>
              <ChefHat size={32} color="#667eea" />
            </div>
            <h1 style={{
              fontSize: '2rem',
              fontWeight: 700,
              color: 'white',
              textShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
            }}>
              Recipe Extractor & Meal Planner
            </h1>
          </div>
          <p style={{
            color: 'rgba(255, 255, 255, 0.9)',
            fontSize: '1.125rem'
          }}>
            Extract recipes from any URL with AI-powered analysis
          </p>
        </header>

        {/* Tabs */}
        <div className="tab-container">
          <button
            className={`tab ${activeTab === 'extract' ? 'active' : ''}`}
            onClick={() => setActiveTab('extract')}
          >
            <Sparkles size={18} />
            Extract Recipe
          </button>
          <button
            className={`tab ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            <History size={18} />
            Saved Recipes
          </button>
        </div>

        {/* Content */}
        <div className="fade-in">
          {activeTab === 'extract' && (
            <RecipeExtractor onRecipeExtracted={handleRecipeExtracted} />
          )}
          {activeTab === 'history' && (
            <RecipeHistory key={refreshHistory} />
          )}
        </div>

        {/* Footer */}
        <footer style={{
          textAlign: 'center',
          marginTop: '3rem',
          padding: '2rem',
          color: 'rgba(255, 255, 255, 0.7)',
          fontSize: '0.875rem'
        }}>
          <p>Powered by FastAPI, React & Google Gemini AI</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
