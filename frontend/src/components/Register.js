import React, { useState, useEffect } from 'react';
import * as api from '../api';

function Register({ onRegister, switchToLogin }) {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    discord_username: '',
    games: []
  });
  const [availableGames, setAvailableGames] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.getGames().then(setAvailableGames).catch(console.error);
  }, []);

  const handleGameToggle = (gameId) => {
    setFormData(prev => {
      const gameExists = prev.games.find(g => g.game_id === gameId);
      if (gameExists) {
        return { ...prev, games: prev.games.filter(g => g.game_id !== gameId) };
      }
      return { ...prev, games: [...prev.games, { game_id: gameId, skill_level: 'intermediate' }] };
    });
  };

  const handleSkillChange = (gameId, skillLevel) => {
    setFormData(prev => ({
      ...prev,
      games: prev.games.map(g => 
        g.game_id === gameId ? { ...g, skill_level: skillLevel } : g
      )
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (formData.games.length === 0) {
      setError('Please select at least one game');
      setLoading(false);
      return;
    }

    try {
      const response = await api.register(formData);
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      onRegister(response.user);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const skillLevels = ['beginner', 'intermediate', 'advanced', 'expert'];

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>🎮 TeamFinder</h1>
        <h2>Create Account</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              required
              placeholder="Choose a username"
            />
          </div>

          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
              placeholder="your@email.com"
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
              minLength={6}
              placeholder="At least 6 characters"
            />
          </div>

          <div className="form-group">
            <label>Discord Username</label>
            <input
              type="text"
              value={formData.discord_username}
              onChange={(e) => setFormData({ ...formData, discord_username: e.target.value })}
              required
              placeholder="username#0000 or username"
            />
          </div>

          <div className="form-group">
            <label>Select Your Games & Skill Level</label>
            <div className="games-selection">
              {availableGames.map(game => {
                const selectedGame = formData.games.find(g => g.game_id === game.id);
                return (
                  <div key={game.id} className={`game-card ${selectedGame ? 'selected' : ''}`}>
                    <div 
                      className="game-header"
                      onClick={() => handleGameToggle(game.id)}
                    >
                      <span className="game-icon">{game.icon}</span>
                      <span className="game-name">{game.name}</span>
                      <span className="game-checkbox">{selectedGame ? '✓' : '+'}</span>
                    </div>
                    {selectedGame && (
                      <select
                        value={selectedGame.skill_level}
                        onChange={(e) => handleSkillChange(game.id, e.target.value)}
                        onClick={(e) => e.stopPropagation()}
                      >
                        {skillLevels.map(level => (
                          <option key={level} value={level}>
                            {level.charAt(0).toUpperCase() + level.slice(1)}
                          </option>
                        ))}
                      </select>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <p className="switch-auth">
          Already have an account?{' '}
          <button type="button" onClick={switchToLogin} className="btn-link">
            Login
          </button>
        </p>
      </div>
    </div>
  );
}

export default Register;
