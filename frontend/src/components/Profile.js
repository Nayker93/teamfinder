import React, { useState, useEffect } from 'react';
import * as api from '../api';

function Profile({ user, onLogout }) {
  const [profile, setProfile] = useState(null);
  const [availableGames, setAvailableGames] = useState([]);
  const [selectedGames, setSelectedGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [profileData, gamesData] = await Promise.all([
        api.getProfile(),
        api.getGames()
      ]);
      setProfile(profileData);
      setAvailableGames(gamesData);
      setSelectedGames(profileData.games.map(g => ({
        game_id: g.game_id,
        skill_level: g.skill_level
      })));
    } catch (err) {
      console.error('Failed to load profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGameToggle = (gameId) => {
    setSelectedGames(prev => {
      const gameExists = prev.find(g => g.game_id === gameId);
      if (gameExists) {
        return prev.filter(g => g.game_id !== gameId);
      }
      return [...prev, { game_id: gameId, skill_level: 'intermediate' }];
    });
  };

  const handleSkillChange = (gameId, skillLevel) => {
    setSelectedGames(prev => prev.map(g => 
      g.game_id === gameId ? { ...g, skill_level: skillLevel } : g
    ));
  };

  const savePreferences = async () => {
    setSaving(true);
    setMessage('');
    try {
      await api.updateGamePreferences(selectedGames);
      setMessage('Preferences saved successfully!');
      setTimeout(() => setMessage(''), 3000);
    } catch (err) {
      setMessage('Failed to save preferences');
    } finally {
      setSaving(false);
    }
  };

  const getSkillBadgeColor = (level) => {
    const colors = {
      beginner: '#4CAF50',
      intermediate: '#2196F3',
      advanced: '#FF9800',
      expert: '#F44336'
    };
    return colors[level] || '#9E9E9E';
  };

  const skillLevels = ['beginner', 'intermediate', 'advanced', 'expert'];

  if (loading) {
    return (
      <div className="profile-container">
        <div className="loading">Loading profile...</div>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <div className="profile-avatar">👤</div>
        <div className="profile-info">
          <h2>{profile?.username}</h2>
          <p className="profile-email">{profile?.email}</p>
          <div className="profile-discord">
            <span className="discord-icon">💬</span>
            <span>{profile?.discord_username}</span>
          </div>
        </div>
        <button className="btn-logout" onClick={onLogout}>
          Logout
        </button>
      </div>

      <div className="profile-section">
        <h3>🎮 Your Games</h3>
        <p className="section-subtitle">Select games you play and your skill level</p>

        {message && (
          <div className={`message ${message.includes('success') ? 'success' : 'error'}`}>
            {message}
          </div>
        )}

        <div className="games-grid">
          {availableGames.map(game => {
            const selectedGame = selectedGames.find(g => g.game_id === game.id);
            return (
              <div 
                key={game.id} 
                className={`game-preference-card ${selectedGame ? 'selected' : ''}`}
              >
                <div 
                  className="game-preference-header"
                  onClick={() => handleGameToggle(game.id)}
                >
                  <span className="game-icon">{game.icon}</span>
                  <span className="game-name">{game.name}</span>
                  <span className="game-checkbox">{selectedGame ? '✓' : '+'}</span>
                </div>
                {selectedGame && (
                  <div className="skill-selector">
                    {skillLevels.map(level => (
                      <button
                        key={level}
                        className={`skill-btn ${selectedGame.skill_level === level ? 'active' : ''}`}
                        style={selectedGame.skill_level === level ? { backgroundColor: getSkillBadgeColor(level) } : {}}
                        onClick={() => handleSkillChange(game.id, level)}
                      >
                        {level.charAt(0).toUpperCase() + level.slice(1)}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <button 
          className="btn-primary save-btn" 
          onClick={savePreferences}
          disabled={saving}
        >
          {saving ? 'Saving...' : 'Save Preferences'}
        </button>
      </div>
    </div>
  );
}

export default Profile;
