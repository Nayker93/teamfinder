import React, { useState, useEffect } from 'react';
import * as api from '../api';

function Matches({ user }) {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMatches();
  }, []);

  const loadMatches = async () => {
    try {
      const confirmedMatches = await api.getConfirmedMatches();
      setMatches(confirmedMatches);
    } catch (err) {
      console.error('Failed to load matches:', err);
    } finally {
      setLoading(false);
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

  if (loading) {
    return (
      <div className="matches-container">
        <h2>🤝 Your Matches</h2>
        <div className="loading">Loading your matches...</div>
      </div>
    );
  }

  return (
    <div className="matches-container">
      <h2>🤝 Your Matches</h2>
      <p className="subtitle">Players who want to team up with you</p>

      {matches.length === 0 ? (
        <div className="no-matches-message">
          <h3>😔 No matches yet</h3>
          <p>Keep swiping to find teammates!</p>
        </div>
      ) : (
        <div className="matches-grid">
          {matches.map((match, index) => (
            <div key={`${match.id}-${match.game_id}-${index}`} className="match-item">
              <div className="match-item-header">
                <div className="match-avatar-small">👤</div>
                <div className="match-info">
                  <h3>{match.username}</h3>
                  <div className="match-game-info">
                    <span>{match.game_icon}</span>
                    <span>{match.game_name}</span>
                  </div>
                </div>
                <span 
                  className="skill-badge small"
                  style={{ backgroundColor: getSkillBadgeColor(match.skill_level) }}
                >
                  {match.skill_level}
                </span>
              </div>
              <div className="discord-section">
                <span className="discord-label">Discord:</span>
                <span className="discord-value">
                  <span className="discord-icon">💬</span>
                  {match.discord_username}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Matches;
