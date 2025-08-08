import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './OutputPage.css';

const OutputPage = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('summary');
  const [analysisResult, setAnalysisResult] = useState(null);

  useEffect(() => {
    const result = localStorage.getItem('analysisResult');
    if (result) {
      setAnalysisResult(JSON.parse(result));
    } else {
      // If no result, redirect back to input form
      navigate('/');
    }
  }, [navigate]);

  if (!analysisResult) {
    return (
      <div className="container">
        <div className="loading">
          <div className="spinner"></div>
          <span>Loading results...</span>
        </div>
      </div>
    );
  }

  const renderSummary = () => (
    <div className="output-section">
      <h3>Analysis Results</h3>
      <div className="summary-content">
        {analysisResult.output ? (
          <pre className="output-text">{analysisResult.output}</pre>
        ) : (
          <p>No analysis results available</p>
        )}
      </div>
    </div>
  );

  const renderKeyInsights = () => (
    <div className="output-section">
      <h3>Key Insights</h3>
      <div className="insights-content">
        {analysisResult.key_insights && analysisResult.key_insights.length > 0 ? (
          <ul className="insights-list">
            {analysisResult.key_insights.map((insight, index) => (
              <li key={index} className="insight-item">
                <span className="insight-bullet">•</span>
                <span className="insight-text">{insight}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p>No key insights available</p>
        )}
      </div>
    </div>
  );

  const renderRecommendations = () => (
    <div className="output-section">
      <h3>Recommendations</h3>
      <div className="recommendations-content">
        {analysisResult.recommendations && analysisResult.recommendations.length > 0 ? (
          <ul className="recommendations-list">
            {analysisResult.recommendations.map((recommendation, index) => (
              <li key={index} className="recommendation-item">
                <span className="recommendation-number">{index + 1}.</span>
                <span className="recommendation-text">{recommendation}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p>No recommendations available</p>
        )}
      </div>
    </div>
  );

  const renderDetailedAnalysis = () => (
    <div className="output-section">
      <h3>Detailed Analysis</h3>
      <div className="detailed-content">
        {analysisResult.detailed_analysis ? (
          <div className="analysis-text">
            {analysisResult.detailed_analysis.split('\n').map((paragraph, index) => (
              <p key={index}>{paragraph}</p>
            ))}
          </div>
        ) : (
          <p>No detailed analysis available</p>
        )}
      </div>
    </div>
  );

  const renderRawData = () => (
    <div className="output-section">
      <h3>Raw Analysis Data</h3>
      <div className="raw-data-content">
        <pre className="json-display">
          {JSON.stringify(analysisResult, null, 2)}
        </pre>
      </div>
    </div>
  );

  const renderTabContent = () => {
    return renderSummary();
  };

  return (
    <div className="container">
      <div className="output-container">
        <div className="output-header">
          <h2>Analysis Results</h2>
          <button 
            className="new-analysis-btn"
            onClick={() => {
              localStorage.removeItem('analysisResult');
              navigate('/');
            }}
          >
            Start New Analysis
          </button>
        </div>

        <div className="nav-tabs">
          <button
            className={`nav-tab active`}
            onClick={() => setActiveTab('summary')}
          >
            Analysis Results
          </button>
        </div>

        <div className="tab-content">
          {renderTabContent()}
        </div>
      </div>
    </div>
  );
};

export default OutputPage;
