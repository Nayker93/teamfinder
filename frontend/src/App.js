import React, { useState, useEffect } from 'react';
import './App.css';
import Login from './components/Login';
import Register from './components/Register';
import Matchmaking from './components/Matchmaking';
import Matches from './components/Matches';
import Profile from './components/Profile';
import Navigation from './components/Navigation';

function App() {
  const [user, setUser] = useState(null);
  const [authMode, setAuthMode] = useState('login');
  const [currentPage, setCurrentPage] = useState('matchmaking');

  useEffect(() => {
    // Check for existing session
    const savedUser = localStorage.getItem('user');
    const token = localStorage.getItem('token');
    if (savedUser && token) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setCurrentPage('matchmaking');
  };

  // Not logged in - show auth screens
  if (!user) {
    if (authMode === 'login') {
      return (
        <Login 
          onLogin={handleLogin} 
          switchToRegister={() => setAuthMode('register')} 
        />
      );
    }
    return (
      <Register 
        onRegister={handleLogin} 
        switchToLogin={() => setAuthMode('login')} 
      />
    );
  }

  // Logged in - show main app
  return (
    <div className="app">
      <header className="app-header">
        <h1>🎮 TeamFinder</h1>
      </header>
      
      <main className="app-content">
        {currentPage === 'matchmaking' && <Matchmaking user={user} />}
        {currentPage === 'matches' && <Matches user={user} />}
        {currentPage === 'profile' && <Profile user={user} onLogout={handleLogout} />}
      </main>

      <Navigation currentPage={currentPage} setCurrentPage={setCurrentPage} />
    </div>
  );
}

export default App;
