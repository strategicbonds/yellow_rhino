import React from 'react';
import logo from './logo.png';
import './App.css';
import Header from './Components/HeaderOne'; // Adjust the path if necessary

function App() {
  return (
    <div className="App">
      <div className="App-header">
      <Header />
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          a data driven car buying experience
        </p>
        <a
          className="App-link"
          href="https://frontend-yellow-rhino-d42f892b13c8.herokuapp.com/"
          target="_blank"
          rel="noopener noreferrer" // Fix the rel attribute
        >
          Yellow Rhino
        </a>
      </div>
    </div>
  );
}

export default App;
