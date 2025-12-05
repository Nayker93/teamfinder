# TeamFinder 🎮

Application web de matchmaking pour joueurs de jeux vidéo - Trouvez votre coéquipier idéal !

## Description

TeamFinder est une application web inspirée des applications de rencontre, mais pour les gamers. Elle permet de trouver des coéquipiers pour vos jeux préférés (League of Legends, Rocket League, Fortnite, etc.) en fonction de vos préférences de jeu et de votre niveau de compétence.

### Fonctionnalités principales

- 🎯 **Matchmaking par jeu** : Trouvez des joueurs qui jouent aux mêmes jeux que vous
- 📊 **Niveau de compétence** : Filtrez par niveau (débutant, intermédiaire, avancé, expert)
- 👍 **Système de swipe** : Likez ou passez les profils de joueurs potentiels
- 🤝 **Match mutuel** : Quand deux joueurs se likent mutuellement, c'est un match !
- 💬 **Discord révélé** : Une fois le match confirmé, accédez au pseudo Discord de votre nouveau coéquipier

## Jeux supportés

- League of Legends 🎮
- Rocket League 🚗
- Fortnite 🔫
- Valorant 🎯
- Counter-Strike 2 💣
- Apex Legends 🦾
- Overwatch 2 🦸
- Minecraft ⛏️

## Technologies

### Backend
- Node.js avec Express
- SQLite (better-sqlite3)
- JWT pour l'authentification
- bcryptjs pour le hachage des mots de passe

### Frontend
- React
- CSS moderne avec gradients et glassmorphism

## Installation

### Prérequis
- Node.js (v16 ou supérieur)
- npm

### Backend

```bash
cd backend
npm install
npm start
```

Le serveur démarre sur `http://localhost:3001`

### Frontend

```bash
cd frontend
npm install
npm start
```

L'application démarre sur `http://localhost:3000`

## Utilisation

1. **Créer un compte** : Entrez votre nom d'utilisateur, email, mot de passe, et pseudo Discord
2. **Sélectionner vos jeux** : Choisissez les jeux auxquels vous jouez et votre niveau
3. **Trouver des coéquipiers** : Naviguez vers "Find" et sélectionnez un jeu
4. **Swiper** : Likez ou passez les profils de joueurs
5. **Matcher** : Quand vous avez un match mutuel, le pseudo Discord de l'autre joueur est révélé !
6. **Voir vos matchs** : Accédez à tous vos matchs confirmés dans l'onglet "Matches"

## Structure du projet

```
teamfinder/
├── backend/
│   ├── server.js      # API Express
│   ├── database.js    # Configuration SQLite
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Matchmaking.js
│   │   │   ├── Matches.js
│   │   │   ├── Profile.js
│   │   │   └── Navigation.js
│   │   ├── api.js
│   │   ├── App.js
│   │   └── App.css
│   └── package.json
└── README.md
```

## API Endpoints

### Authentification
- `POST /api/register` - Créer un compte
- `POST /api/login` - Se connecter

### Jeux
- `GET /api/games` - Liste des jeux disponibles

### Profil
- `GET /api/profile` - Profil de l'utilisateur connecté
- `PUT /api/profile/games` - Mettre à jour les préférences de jeux
- `GET /api/user/games` - Jeux de l'utilisateur connecté

### Matchmaking
- `GET /api/matches/potential/:gameId` - Joueurs potentiels pour un jeu
- `POST /api/matches/action` - Liker ou passer un profil
- `GET /api/matches/confirmed` - Matchs confirmés (mutuels)

## Licence

MIT
