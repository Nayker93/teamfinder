const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const rateLimit = require('express-rate-limit');
const db = require('./database');

const app = express();
const PORT = process.env.PORT || 3001;
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) {
  console.warn('WARNING: JWT_SECRET environment variable is not set. Using a random secret for development only.');
}
const jwtSecret = JWT_SECRET || require('crypto').randomBytes(32).toString('hex');

app.use(cors());
app.use(express.json());

// Rate limiting middleware
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later.' }
});

// Stricter rate limit for authentication endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // Limit each IP to 10 auth requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many authentication attempts, please try again later.' }
});

// Apply general rate limiting to all requests
app.use(limiter);

// Middleware to verify JWT token
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, jwtSecret, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }
    req.user = user;
    next();
  });
}

// Register a new user
app.post('/api/register', authLimiter, async (req, res) => {
  try {
    const { username, email, password, discord_username, games } = req.body;

    if (!username || !email || !password || !discord_username) {
      return res.status(400).json({ error: 'All fields are required' });
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const insertUser = db.prepare(
      'INSERT INTO users (username, email, password, discord_username) VALUES (?, ?, ?, ?)'
    );
    
    const result = insertUser.run(username, email, hashedPassword, discord_username);
    const userId = result.lastInsertRowid;

    // Add user game preferences
    if (games && games.length > 0) {
      const insertUserGame = db.prepare(
        'INSERT INTO user_games (user_id, game_id, skill_level) VALUES (?, ?, ?)'
      );
      for (const game of games) {
        insertUserGame.run(userId, game.game_id, game.skill_level);
      }
    }

    const token = jwt.sign({ id: userId, username }, jwtSecret, { expiresIn: '7d' });

    res.status(201).json({ 
      message: 'User registered successfully',
      token,
      user: { id: userId, username, email, discord_username }
    });
  } catch (error) {
    if (error.message.includes('UNIQUE constraint failed')) {
      return res.status(400).json({ error: 'Username or email already exists' });
    }
    res.status(500).json({ error: 'Registration failed' });
  }
});

// Login
app.post('/api/login', authLimiter, async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    const user = db.prepare('SELECT * FROM users WHERE email = ?').get(email);

    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const validPassword = await bcrypt.compare(password, user.password);
    if (!validPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const token = jwt.sign({ id: user.id, username: user.username }, jwtSecret, { expiresIn: '7d' });

    res.json({ 
      token,
      user: { id: user.id, username: user.username, email: user.email, discord_username: user.discord_username }
    });
  } catch (error) {
    res.status(500).json({ error: 'Login failed' });
  }
});

// Get all supported games
app.get('/api/games', (req, res) => {
  try {
    const games = db.prepare('SELECT * FROM games').all();
    res.json(games);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch games' });
  }
});

// Get current user profile with games
app.get('/api/profile', authenticateToken, (req, res) => {
  try {
    const user = db.prepare(`
      SELECT id, username, email, discord_username, created_at 
      FROM users WHERE id = ?
    `).get(req.user.id);

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    const userGames = db.prepare(`
      SELECT ug.*, g.name as game_name, g.icon as game_icon
      FROM user_games ug
      JOIN games g ON ug.game_id = g.id
      WHERE ug.user_id = ?
    `).all(req.user.id);

    res.json({ ...user, games: userGames });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch profile' });
  }
});

// Update user's game preferences
app.put('/api/profile/games', authenticateToken, (req, res) => {
  try {
    const { games } = req.body;
    const userId = req.user.id;

    // Delete existing game preferences
    db.prepare('DELETE FROM user_games WHERE user_id = ?').run(userId);

    // Insert new game preferences
    if (games && games.length > 0) {
      const insertUserGame = db.prepare(
        'INSERT INTO user_games (user_id, game_id, skill_level) VALUES (?, ?, ?)'
      );
      for (const game of games) {
        insertUserGame.run(userId, game.game_id, game.skill_level);
      }
    }

    res.json({ message: 'Game preferences updated successfully' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to update game preferences' });
  }
});

// Get potential matches for a specific game
app.get('/api/matches/potential/:gameId', authenticateToken, (req, res) => {
  try {
    const { gameId } = req.params;
    const userId = req.user.id;

    // Find users who play the same game and haven't been matched yet
    const potentialMatches = db.prepare(`
      SELECT u.id, u.username, ug.skill_level, g.name as game_name, g.icon as game_icon
      FROM users u
      JOIN user_games ug ON u.id = ug.user_id
      JOIN games g ON ug.game_id = g.id
      WHERE ug.game_id = ?
      AND u.id != ?
      AND u.id NOT IN (
        SELECT target_user_id FROM matches 
        WHERE user_id = ? AND game_id = ?
      )
      ORDER BY RANDOM()
      LIMIT 10
    `).all(gameId, userId, userId, gameId);

    res.json(potentialMatches);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch potential matches' });
  }
});

// Like or pass on a potential match
app.post('/api/matches/action', authenticateToken, (req, res) => {
  try {
    const { targetUserId, gameId, action } = req.body;
    const userId = req.user.id;

    if (!['liked', 'passed'].includes(action)) {
      return res.status(400).json({ error: 'Invalid action' });
    }

    // Insert the match action
    const insertMatch = db.prepare(`
      INSERT OR REPLACE INTO matches (user_id, target_user_id, game_id, status)
      VALUES (?, ?, ?, ?)
    `);
    insertMatch.run(userId, targetUserId, gameId, action);

    // Check if it's a mutual match
    let isMatch = false;
    let matchedUser = null;

    if (action === 'liked') {
      const mutualMatch = db.prepare(`
        SELECT * FROM matches 
        WHERE user_id = ? AND target_user_id = ? AND game_id = ? AND status = 'liked'
      `).get(targetUserId, userId, gameId);

      if (mutualMatch) {
        isMatch = true;
        // Get the matched user's discord username
        matchedUser = db.prepare(`
          SELECT u.id, u.username, u.discord_username, ug.skill_level, g.name as game_name
          FROM users u
          JOIN user_games ug ON u.id = ug.user_id AND ug.game_id = ?
          JOIN games g ON g.id = ?
          WHERE u.id = ?
        `).get(gameId, gameId, targetUserId);
      }
    }

    res.json({ 
      message: action === 'liked' ? 'User liked' : 'User passed',
      isMatch,
      matchedUser
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to process match action' });
  }
});

// Get all confirmed matches (mutual likes)
app.get('/api/matches/confirmed', authenticateToken, (req, res) => {
  try {
    const userId = req.user.id;

    const confirmedMatches = db.prepare(`
      SELECT DISTINCT
        u.id,
        u.username,
        u.discord_username,
        g.id as game_id,
        g.name as game_name,
        g.icon as game_icon,
        ug.skill_level
      FROM matches m1
      JOIN matches m2 ON m1.target_user_id = m2.user_id 
        AND m1.user_id = m2.target_user_id 
        AND m1.game_id = m2.game_id
      JOIN users u ON u.id = m1.target_user_id
      JOIN games g ON g.id = m1.game_id
      JOIN user_games ug ON ug.user_id = u.id AND ug.game_id = g.id
      WHERE m1.user_id = ? 
        AND m1.status = 'liked' 
        AND m2.status = 'liked'
    `).all(userId);

    res.json(confirmedMatches);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch confirmed matches' });
  }
});

// Get user's games for matchmaking selection
app.get('/api/user/games', authenticateToken, (req, res) => {
  try {
    const userGames = db.prepare(`
      SELECT g.id, g.name, g.icon, ug.skill_level
      FROM user_games ug
      JOIN games g ON ug.game_id = g.id
      WHERE ug.user_id = ?
    `).all(req.user.id);

    res.json(userGames);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch user games' });
  }
});

app.listen(PORT, () => {
  console.log(`TeamFinder backend running on port ${PORT}`);
});

module.exports = app;
