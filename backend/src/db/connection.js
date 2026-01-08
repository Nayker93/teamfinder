import { Pool } from 'pg';
import dotenv from 'dotenv';

dotenv.config();

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://teamfinder:devpassword123@localhost:5432/teamfinder',
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

pool.connect()
  .then(() => console.log('✅ PostgreSQL connecté avec succès !'))
  .catch(err => console.error('❌ Erreur DB:', err.message));

// Export pour utilisation
export default pool;
