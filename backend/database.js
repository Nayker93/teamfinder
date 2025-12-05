const Database = require('better-sqlite3');
const path = require('path');

const dbPath = process.env.DB_PATH || path.join(__dirname, 'teamfinder.db');
const db = new Database(dbPath);

// Initialize database schema
function initializeDatabase() {
  // Users table
  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      email TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL,
      discord_username TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Games table (supported games)
  db.exec(`
    CREATE TABLE IF NOT EXISTS games (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT UNIQUE NOT NULL,
      icon TEXT
    )
  `);

  // User game preferences (which games they play and at what level)
  db.exec(`
    CREATE TABLE IF NOT EXISTS user_games (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      game_id INTEGER NOT NULL,
      skill_level TEXT NOT NULL CHECK(skill_level IN ('beginner', 'intermediate', 'advanced', 'expert')),
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
      FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
      UNIQUE(user_id, game_id)
    )
  `);

  // Matches table (tracks likes/dislikes between users for specific games)
  db.exec(`
    CREATE TABLE IF NOT EXISTS matches (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      target_user_id INTEGER NOT NULL,
      game_id INTEGER NOT NULL,
      status TEXT NOT NULL CHECK(status IN ('pending', 'liked', 'passed')),
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
      FOREIGN KEY (target_user_id) REFERENCES users(id) ON DELETE CASCADE,
      FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
      UNIQUE(user_id, target_user_id, game_id)
    )
  `);

  // Insert default games if not exists
  const defaultGames = [
    { name: 'League of Legends', icon: '🎮' },
    { name: 'Rocket League', icon: '🚗' },
    { name: 'Fortnite', icon: '🔫' },
    { name: 'Valorant', icon: '🎯' },
    { name: 'Counter-Strike 2', icon: '💣' },
    { name: 'Apex Legends', icon: '🦾' },
    { name: 'Overwatch 2', icon: '🦸' },
    { name: 'Minecraft', icon: '⛏️' }
  ];

  const insertGame = db.prepare('INSERT OR IGNORE INTO games (name, icon) VALUES (?, ?)');
  for (const game of defaultGames) {
    insertGame.run(game.name, game.icon);
  }
}

initializeDatabase();

module.exports = db;
