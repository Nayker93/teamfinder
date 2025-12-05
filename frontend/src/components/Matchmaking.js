import React, { useState, useEffect } from 'react';
import * as api from '../api';

function Matchmaking({ user }) {
  const [userGames, setUserGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null);
  const [potentialMatches, setPotentialMatches] = useState([]);
  const [currentMatchIndex, setCurrentMatchIndex] = useState(0);
  const [notification, setNotification] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadUserGames();
  }, []);

  const loadUserGames = async () => {
    try {
      const games = await api.getUserGames();
      setUserGames(games);
    } catch (err) {
      console.error('Failed to load user games:', err);
    }
  };

  const selectGame = async (game) => {
    setSelectedGame(game);
    setLoading(true);
    try {
      const matches = await api.getPotentialMatches(game.id);
      setPotentialMatches(matches);
      setCurrentMatchIndex(0);
    } catch (err) {
      console.error('Failed to load potential matches:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (action) => {
    const currentMatch = potentialMatches[currentMatchIndex];
    if (!currentMatch) return;

    try {
      const result = await api.matchAction(currentMatch.id, selectedGame.id, action);
      
      if (result.isMatch) {
        setNotification({
          type: 'match',
          user: result.matchedUser
        });
      }

      // Move to next match
      if (currentMatchIndex < potentialMatches.length - 1) {
        setCurrentMatchIndex(prev => prev + 1);
      } else {
        // Reload potential matches
        const matches = await api.getPotentialMatches(selectedGame.id);
        setPotentialMatches(matches);
        setCurrentMatchIndex(0);
      }
    } catch (err) {
      console.error('Failed to process action:', err);
    }
  };

  const closeNotification = () => {
    setNotification(null);
  };

  const goBack = () => {
    setSelectedGame(null);
    setPotentialMatches([]);
    setCurrentMatchIndex(0);
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

  if (!selectedGame) {
    return (
      <div className="matchmaking-container">
        <h2>🎮 Find a Teammate</h2>
        <p className="subtitle">Select a game to start matchmaking</p>
        
        <div className="game-selection-grid">
          {userGames.map(game => (
            <div 
              key={game.id} 
              className="game-select-card"
              onClick={() => selectGame(game)}
            >
              <span className="game-icon-large">{game.icon}</span>
              <h3>{game.name}</h3>
              <span 
                className="skill-badge"
                style={{ backgroundColor: getSkillBadgeColor(game.skill_level) }}
              >
                {game.skill_level}
              </span>
            </div>
          ))}
        </div>

        {userGames.length === 0 && (
          <div className="no-games-message">
            <p>You haven't selected any games yet!</p>
            <p>Go to your profile to add games you play.</p>
          </div>
        )}
      </div>
    );
  }

  const currentMatch = potentialMatches[currentMatchIndex];

  return (
    <div className="matchmaking-container">
      {notification && (
        <div className="notification-overlay" onClick={closeNotification}>
          <div className="notification-card match-notification" onClick={e => e.stopPropagation()}>
            <h2>🎉 It's a Match!</h2>
            <p>You and <strong>{notification.user.username}</strong> want to play together!</p>
            <div className="discord-reveal">
              <p>Discord Username:</p>
              <div className="discord-username">
                <span className="discord-icon">💬</span>
                <strong>{notification.user.discord_username}</strong>
              </div>
              <p className="discord-hint">Add them on Discord to start playing!</p>
            </div>
            <button className="btn-primary" onClick={closeNotification}>
              Continue Matching
            </button>
          </div>
        </div>
      )}

      <div className="matchmaking-header">
        <button className="btn-back" onClick={goBack}>← Back</button>
        <div className="current-game">
          <span>{selectedGame.icon}</span>
          <span>{selectedGame.name}</span>
        </div>
      </div>

      {loading ? (
        <div className="loading">Finding teammates...</div>
      ) : currentMatch ? (
        <div className="match-card">
          <div className="match-avatar">
            👤
          </div>
          <h2 className="match-username">{currentMatch.username}</h2>
          <div className="match-game">
            <span>{currentMatch.game_icon}</span>
            <span>{currentMatch.game_name}</span>
          </div>
          <span 
            className="skill-badge large"
            style={{ backgroundColor: getSkillBadgeColor(currentMatch.skill_level) }}
          >
            {currentMatch.skill_level}
          </span>
          
          <div className="match-actions">
            <button 
              className="btn-pass"
              onClick={() => handleAction('passed')}
            >
              ✕ Pass
            </button>
            <button 
              className="btn-like"
              onClick={() => handleAction('liked')}
            >
              ✓ Play Together
            </button>
          </div>
        </div>
      ) : (
        <div className="no-matches">
          <h3>😔 No more teammates available</h3>
          <p>Check back later or try another game!</p>
          <button className="btn-secondary" onClick={goBack}>
            Select Another Game
          </button>
        </div>
      )}
    </div>
  );
}

export default Matchmaking;
