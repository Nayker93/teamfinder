const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

app.get('/api/health', (req, res) => {
  res.json({ 
    status: '✅ Backend OK !',
    port: PORT,
    time: new Date().toISOString()
  });
});

app.get('/api/test', (req, res) => {
  res.json({ message: '🎮 Frontend-Backend connecté !' });
});

app.listen(PORT, () => {
  console.log(`🚀 Backend: http://localhost:${PORT}`);
});
