import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './Landing.jsx'; 
import Dashboard from './Dashboard.jsx'; 

function App() {
  return (
    <Router>  
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/Dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;