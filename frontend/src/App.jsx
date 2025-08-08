import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import InputForm from './components/InputForm';
import OutputPage from './components/OutputPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>InsightLens</h1>
          <p>AI-Powered Document Analysis</p>
        </header>
        <main className="App-main">
          <Routes>
            <Route path="/" element={<InputForm />} />
            <Route path="/output" element={<OutputPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
