import React, { useState, useEffect } from 'react';
import './App.css';
import MergerAnalyzer from './components/MergerAnalyzer';
import CompanyList from './components/CompanyList';
import AnalysisHistory from './components/AnalysisHistory';
import AddCompany from './components/AddCompany';
import api from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('analyze');
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    try {
      setLoading(true);
      const data = await api.getCompanies();
      setCompanies(data.companies);
    } catch (error) {
      console.error('Failed to load companies:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCompanyAdded = () => {
    loadCompanies();
    setActiveTab('analyze');
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <div className="container">
          <h1>🚂 Merger ROI Calculator</h1>
          <p>Research-backed merger analysis platform</p>
        </div>
      </header>

      {/* Navigation */}
      <nav className="app-nav">
        <div className="container">
          <button
            className={`nav-btn ${activeTab === 'analyze' ? 'active' : ''}`}
            onClick={() => setActiveTab('analyze')}
          >
            📊 Analyze Merger
          </button>
          <button
            className={`nav-btn ${activeTab === 'companies' ? 'active' : ''}`}
            onClick={() => setActiveTab('companies')}
          >
            🏢 Companies
          </button>
          <button
            className={`nav-btn ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            📈 History
          </button>
          <button
            className={`nav-btn ${activeTab === 'add' ? 'active' : ''}`}
            onClick={() => setActiveTab('add')}
          >
            ➕ Add Company
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="app-main">
        <div className="container">
          {loading && activeTab === 'analyze' ? (
            <div className="loading">Loading companies...</div>
          ) : (
            <>
              {activeTab === 'analyze' && (
                <MergerAnalyzer companies={companies} />
              )}
              {activeTab === 'companies' && (
                <CompanyList companies={companies} onRefresh={loadCompanies} />
              )}
              {activeTab === 'history' && (
                <AnalysisHistory />
              )}
              {activeTab === 'add' && (
                <AddCompany onCompanyAdded={handleCompanyAdded} />
              )}
            </>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="container">
          <p>Based on research from Damodaran (NYU), Bruner, and Koller (McKinsey)</p>
          <p>© 2026 Merger ROI Calculator | Deployed on Railway</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
