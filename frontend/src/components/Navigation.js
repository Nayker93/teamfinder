import React from 'react';

function Navigation({ currentPage, setCurrentPage }) {
  const navItems = [
    { id: 'matchmaking', label: 'Find', icon: '🎮' },
    { id: 'matches', label: 'Matches', icon: '🤝' },
    { id: 'profile', label: 'Profile', icon: '👤' }
  ];

  return (
    <nav className="bottom-nav">
      {navItems.map(item => (
        <button
          key={item.id}
          className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
          onClick={() => setCurrentPage(item.id)}
        >
          <span className="nav-icon">{item.icon}</span>
          <span className="nav-label">{item.label}</span>
        </button>
      ))}
    </nav>
  );
}

export default Navigation;
