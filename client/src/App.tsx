import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useState, useEffect } from 'react';

import HomePage from './pages/Home/HomePage';
import SearchPage from './pages/Search/SearchPage';
import SearchBar from './components/SearchBar/SearchBar';

function App() {

  return (
    <div>
      <Router>
        <Routes>
          <Route path='/' element={<HomePage/>} />
          <Route path='/search' element={<SearchPage/>} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
