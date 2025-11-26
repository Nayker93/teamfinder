const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

// Get auth token from localStorage
const getToken = () => localStorage.getItem('token');

// Helper function for API calls
async function apiCall(endpoint, options = {}) {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.error || 'API request failed');
  }
  
  return data;
}

// Auth API
export const register = (userData) => apiCall('/register', {
  method: 'POST',
  body: JSON.stringify(userData),
});

export const login = (credentials) => apiCall('/login', {
  method: 'POST',
  body: JSON.stringify(credentials),
});

// Games API
export const getGames = () => apiCall('/games');

// Profile API
export const getProfile = () => apiCall('/profile');
export const updateGamePreferences = (games) => apiCall('/profile/games', {
  method: 'PUT',
  body: JSON.stringify({ games }),
});

// User Games API
export const getUserGames = () => apiCall('/user/games');

// Matchmaking API
export const getPotentialMatches = (gameId) => apiCall(`/matches/potential/${gameId}`);
export const matchAction = (targetUserId, gameId, action) => apiCall('/matches/action', {
  method: 'POST',
  body: JSON.stringify({ targetUserId, gameId, action }),
});
export const getConfirmedMatches = () => apiCall('/matches/confirmed');
