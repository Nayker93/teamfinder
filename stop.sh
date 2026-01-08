#!/bin/bash
echo "🛑 Arrêt TeamFinder..."

# Arrêter Docker
docker-compose down

# Tuer processus Node (si oubli)
pkill -f "npm run dev" 2>/dev/null || true

echo "✅ TeamFinder arrêté"
