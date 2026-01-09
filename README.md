# 🎮 **TeamFinder**

[![React](https://img.shields.io/badge/React-18.2-blue?style=for-the-badge&logo=react)](https://react.dev)
[![Node.js](https://img.shields.io/badge/Node-20-green?style=for-the-badge&logo=node.js)](https://nodejs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-violet?style=for-the-badge&logo=postgresql)](https://postgresql.org)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.3-cyan?style=for-the-badge&logo=tailwind)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Docker-blue?style=for-the-badge&logo=docker)](https://docker.com)

**Plateforme de matchmaking gaming**  
*Trouvez vos coéquipiers parfaits selon votre niveau et vos jeux préférés*  
🤝 **Comme Tinder, mais pour LoL, Rocket League, Valorant...**

## 📱 **Présentation de l'Application**

**TeamFinder** résout un problème majeur des gamers : **trouver le bon coéquipier**.

### 🎯 **Fonctionnalités Clés**

👤 Inscription / Profil multi-jeux (LoL, Rocket League...)
⚡ Matching intelligent par niveau (Bronze, Gold, Diamond...)
❤️ Système Like/Pass bilatéral
💬 Échange Discord après match confirmé
⚡ Temps réel (notifications matchs)

### 🎮 **Exemple d'utilisation**

1. **Inscription** → Ajouter LoL (Gold 2) + Rocket League (Champion)
2. **Découverte** → Voir profils compatibles (Gold/Diamond)
3. **Like** → Si match mutuel → **Discord échangé !**
4. **Jouer** → Victoire garantie avec coéquipier adapté 🎉

### 📊 **Objectif Projet**

👥 Équipe : 4 étudiants ESIEE PARIS B3
🎓 Projet tutoré "Matchmaking Jeux Vidéo"
🚀 MVP : En cours

---

## 🚀 **Démarrage Rapide**

### ✅ **Prérequis**

🔧 Node.js 18+ → [https://nodejs.org]
🐳 Docker Desktop → [https://docker.com]
💻 VSCode + extensions → React, Tailwind CSS IntelliSense
📦 Git → git-scm.com

### 🎬 **Commandes Complètes**

```bash

# Pour lancer avec le script en une commande
./start.sh

# 1. Cloner le projet
git clone https://github.com/VOTRE_USERNAME/teamfinder-app.git
cd teamfinder-app

# 2. Démarrer base de données
docker-compose up -d

# 3. Terminal 1 : Frontend
cd frontend
npm install
npm run dev
# → http://localhost:3000

# 4. Terminal 2 : Backend  
cd ../backend
npm install
npm run dev
# → http://localhost:3001/api/health
```
