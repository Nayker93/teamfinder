#!/bin/bash

# ========================================
# 🚀 TeamFinder - Script de Démarrage Auto
# ========================================

echo "🎮 TeamFinder - Démarrage automatique..."

# Couleurs pour le terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'erreur
error_exit() {
    echo -e "${RED}❌ ERREUR : $1${NC}"
    exit 1
}

# 1. Vérifier Docker
echo -e "${BLUE}🐳 Vérification Docker...${NC}"
docker --version >/dev/null 2>&1 || error_exit "Docker non installé"
docker-compose --version >/dev/null 2>&1 || error_exit "Docker Compose manquant"

# 2. Arrêter services précédents (clean)
echo -e "${BLUE}🧹 Nettoyage services...${NC}"
docker-compose down >/dev/null 2>&1

# 3. Démarrer Docker (DB)
echo -e "${BLUE}🐳 Lancement PostgreSQL...${NC}"
docker-compose up -d postgres
sleep 5  # Attendre DB

# Vérifier DB
if ! docker ps | grep -q teamfinder-db; then
    error_exit "PostgreSQL ne démarre pas"
fi
echo -e "${GREEN}✅ PostgreSQL: http://localhost:5432${NC}"

# 4. Backend
echo -e "${BLUE}⚙️  Backend...${NC}"
cd backend || error_exit "Dossier backend manquant"
npm install >/dev/null 2>&1
cp .env.example .env 2>/dev/null || true
npm run dev &
BACKEND_PID=$!
sleep 3

# Vérifier backend
if ! curl -s http://localhost:3001/api/health >/dev/null; then
    echo -e "${YELLOW}⚠️  Backend lent à démarrer...${NC}"
    sleep 5
fi
echo -e "${GREEN}✅ Backend: http://localhost:3001${NC}"

# 5. Frontend
echo -e "${BLUE}🎨 Frontend...${NC}"
cd ../frontend || error_exit "Dossier frontend manquant"
npm install >/dev/null 2>&1
npm run dev &
FRONTEND_PID=$!
sleep 3
echo -e "${GREEN}✅ Frontend: http://localhost:3000${NC}"

# 6. Status final
echo ""
echo -e "${GREEN}🎉 TeamFinder TOUT DÉMARRÉ !${NC}"
echo ""
echo -e "${BLUE}🌐 URLs:${NC}"
echo "   Frontend : http://localhost:3000"
echo "   Backend  : http://localhost:3001/api/health"
echo "   DB       : localhost:5432 (teamfinder/devpassword123)"
echo ""
echo -e "${YELLOW}🛑 Arrêter : Ctrl+C ou ./stop.sh${NC}"
echo -e "${BLUE}📱 Logs : docker-compose logs -f${NC}"

# Garder script actif
wait $BACKEND_PID $FRONTEND_PID
