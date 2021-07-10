import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {

  const [currentGreetingV1, setCurrentGreetingV1] = useState('Unknown');

  useEffect(() => {
    fetch('/api/greeting/v1/').then(res => res.json()).then(data => {
      setCurrentGreetingV1(data.message);
    })
  })

  return (
    <div className="App">
      <p>The current greeting is {currentGreetingV1}</p>
    </div>
  );
}

export default App;
