// frontend/src/App.js
import React, { useState } from 'react';
import './App.css'; // Assume you have some basic CSS

function App() {
  const [scriptOrSummary, setScriptOrSummary] = useState('');
  const [titles, setTitles] = useState([]);
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    setTitles([]);
    setDescription('');

    try {
      // IMPORTANT: During local development, this URL should point to your Flask backend (http://localhost:5000)
      // When deploying, you'll update this to your deployed backend URL.
      const response = await fetch('http://localhost:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ script_or_summary: scriptOrSummary }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong on the server.');
      }

      setTitles(data.titles);
      setDescription(data.description);

    } catch (err) {
      setError(err.message);
      console.error("Fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    // Simple feedback for the user
    if (navigator.clipboard.writeText) {
        alert('Copied to clipboard!');
    } else {
        alert('Could not copy. Please select and copy manually.');
    }
  };

  return (
    <div className="App">
      <h1>YouTube Video Title & Description Generator</h1>

      <p>Paste your video script or a detailed summary below. The more context, the better!</p>

      <textarea
        value={scriptOrSummary}
        onChange={(e) => setScriptOrSummary(e.target.value)}
        placeholder="e.g., 'In this video, I demonstrate how to fix a leaky faucet in under 10 minutes. I cover tools needed, step-by-step instructions, and common pitfalls to avoid. Focus on DIY and home repair keywords.'"
        rows="10"
        cols="80"
      ></textarea>

      <button onClick={handleSubmit} disabled={loading || !scriptOrSummary.trim()}>
        {loading ? 'Generating...' : 'Generate Titles & Description'}
      </button>

      {error && <p className="error-message">{error}</p>}

      {titles.length > 0 && (
        <div className="output-section">
          <h2>Generated Titles:</h2>
          {titles.map((title, index) => (
            <div key={index} className="output-item">
              <p>{title}</p>
              <button onClick={() => copyToClipboard(title)}>Copy</button>
            </div>
          ))}
        </div>
      )}

      {description && (
        <div className="output-section">
          <h2>Generated Description:</h2>
          <textarea
            value={description}
            readOnly
            rows="15"
            cols="80"
          ></textarea>
          <button onClick={() => copyToClipboard(description)}>Copy Description</button>
        </div>
      )}
    </div>
  );
}

export default App;