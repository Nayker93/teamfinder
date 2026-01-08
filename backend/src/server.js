import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import db from './db/connection.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}));
app.use(express.json());

// Routes de test
app.get('/api/health', async (req, res) => {
  try {
    await db.query('SELECT 1');
    res.json({ 
      status: 'OK', 
      message: 'TeamFinder Backend ✅ DB connectée',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ error: 'DB erreur' });
  }
});

app.get('/api/test', (req, res) => {
  res.json({ message: 'API TeamFinder fonctionne ! 🚀' });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route non trouvée' });
});

// Error handler
app.use((error, req, res, next) => {
  console.error(error);
  res.status(500).json({ error: 'Erreur serveur' });
});

// Démarrage serveur
app.listen(PORT, () => {
  console.log(`🚀 Backend TeamFinder sur http://localhost:${PORT}`);
  console.log(`📊 Testez : http://localhost:${PORT}/api/health`);
});
