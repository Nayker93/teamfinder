#!/usr/bin/env python3
"""
Script pour créer toutes les issues TeamFinder MVP via GitHub API
"""

import requests
import json
import os
from dotenv import load_dotenv
from typing import Dict, List

# Charger les variables d'environnement
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_PROJECT_NUMBER = int(os.getenv("GITHUB_PROJECT_NUMBER", "1"))

# Configuration API
BASE_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

# 🎯 LES 33 ISSUES À CRÉER
ISSUES = [
    # INFRASTRUCTURE (5)
    {
        "title": "INFRA-S1.1 - Setup GitHub repo + branches",
        "body": """## Description
Créer et configurer le dépôt GitHub avec structure branches.

## Acceptance Criteria
- [ ] Repository créé avec .gitignore (node_modules, .env)
- [ ] Branches créées : main, develop, develop-backend, develop-frontend
- [ ] Branch protection sur main (PR review requis)
- [ ] Collaborators ajoutés (4 étudiants)
- [ ] GitHub Projects créé
- [ ] README.md initial avec instruction setup
- [ ] Wiki créé avec conventions

## Implementation
- Initialiser repo avec template Node.js
- Config branch protection (Settings → Branches)
- Add collaborators
- Create Wiki homepage (setup guide)

## Testing
- Cloner repo en local
- Vérifier branche création
- Vérifier protection main""",
        "labels": ["infra", "sprint-1", "p0"],
        "assignee": "[Tech Lead]",
        "estimate": "1h",
    },
    {
        "title": "INFRA-S1.2 - Setup Docker + docker-compose",
        "body": """## Description
Créer Dockerfile backend/frontend et docker-compose.yml pour dev.

## Acceptance Criteria
- [ ] Dockerfile backend (Node 20)
- [ ] Dockerfile frontend (Node 20 + Vite)
- [ ] docker-compose.yml avec 3 services (postgres, backend, frontend)
- [ ] .dockerignore créés
- [ ] Volumes configurés (hot reload)
- [ ] Environment variables dans docker-compose
- [ ] docker-compose up -d fonctionne

## Implementation
- Base image : node:20-alpine
- Multi-stage build (smaller image)
- Network : teamfinder-net
- Volumes : backend/src pour hot reload

## Testing
- docker-compose up -d
- Vérifier 3 services running
- docker-compose logs -f
- Test http://localhost:3000 et 3001""",
        "labels": ["infra", "sprint-1", "p0"],
        "assignee": "[Tech Lead]",
        "estimate": "3h",
    },
    {
        "title": "INFRA-S1.3 - Setup PostgreSQL database",
        "body": """## Description
Créer et initialiser database PostgreSQL avec tables.

## Acceptance Criteria
- [ ] PostgreSQL 15 running in docker
- [ ] Database 'teamfinder_db' créé
- [ ] SQL schema complet créé (users, games, user_games, interactions, matches)
- [ ] Indexes créés
- [ ] Foreign keys avec ON DELETE CASCADE
- [ ] Init script (init.sql) dans backend/sql/
- [ ] psql connection testée

## Implementation
- Image : postgres:15-alpine
- Volume postgres_data persistent
- Init script lancé au startup
- Charset UTF-8

## Testing
- docker-compose exec postgres psql -U teamfinder -d teamfinder_db
- \\dt (vérifier tables)
- SELECT count(*) FROM users;""",
        "labels": ["infra", "database", "sprint-1", "p0"],
        "assignee": "[Backend Lead]",
        "estimate": "2h",
    },
    {
        "title": "INFRA-S1.4 - Setup Vite frontend project",
        "body": """## Description
Initialiser React 18.2 + Vite project avec tooling.

## Acceptance Criteria
- [ ] Vite project créé (npm create vite@latest)
- [ ] React 18.2 + React DOM installés
- [ ] TailwindCSS 3.3 configuré
- [ ] ESLint + Prettier configurés
- [ ] Vitest + @testing-library/react installés
- [ ] package.json scripts configurés (dev, build, test, lint)
- [ ] npm run dev fonctionne
- [ ] Hot reload (HMR) fonctionne

## Testing
- npm install (pas d'erreurs)
- npm run dev → localhost:3000
- Modifier un fichier → HMR auto-reload
- npm run build → dist/ créé""",
        "labels": ["infra", "frontend", "sprint-1", "p0"],
        "assignee": "[Frontend Lead]",
        "estimate": "2h",
    },
    {
        "title": "INFRA-S1.5 - Setup Express backend project",
        "body": """## Description
Initialiser Node.js + Express project avec structure.

## Acceptance Criteria
- [ ] Express 4.x installé + dépendances core
- [ ] Dossier structure (controllers, routes, middleware, services, utils)
- [ ] server.js entry point créé
- [ ] .env + .env.example configurés
- [ ] ESLint + Prettier configurés
- [ ] Jest configuré pour tests
- [ ] Health check endpoint (/api/health) fonctionne
- [ ] npm run dev fonctionne (auto-reload avec Nodemon)

## Testing
- npm install
- npm run dev → http://localhost:3001/api/health""",
        "labels": ["infra", "backend", "sprint-1", "p0"],
        "assignee": "[Backend Lead]",
        "estimate": "2h",
    },

    # BACKEND (7)
    {
        "title": "BACK-S1.1 - Create database schema & migrations",
        "body": """## Description
Créer SQL schema complet avec tables, indexes, foreign keys.

## Acceptance Criteria
- [ ] 5 tables créées (users, games, user_games, interactions, matches)
- [ ] UUIDs en primary keys
- [ ] Foreign keys avec ON DELETE CASCADE
- [ ] Indexes sur user_id, game_id, interactions
- [ ] UNIQUE constraints
- [ ] Timestamps (created_at, updated_at)
- [ ] Schema importable via init.sql

## Testing
- \\d users (describe table)
- SELECT count(*) FROM games;""",
        "labels": ["backend", "database", "sprint-1", "p0"],
        "assignee": "[Backend Lead]",
        "estimate": "2h",
    },
    {
        "title": "BACK-S1.2 - Setup Express auth routes",
        "body": """## Description
Créer structure routes Express + middleware auth.

## Acceptance Criteria
- [ ] routes/authRoutes.js créé
- [ ] POST /api/auth/signup route
- [ ] POST /api/auth/login route
- [ ] POST /api/auth/verify-email route
- [ ] middleware/authMiddleware.js créé
- [ ] CORS configuré
- [ ] Morgan logging configuré
- [ ] Helmet security headers activé

## Testing
- curl -X POST http://localhost:3001/api/auth/signup
- Check routes registered""",
        "labels": ["backend", "auth", "sprint-1", "p0"],
        "assignee": "[Backend Lead]",
        "estimate": "2h",
    },
    {
        "title": "BACK-S1.3 - Implement signup controller",
        "body": """## Description
Implémenter logique complet signup : validation, user creation, email send.

## Acceptance Criteria
- [ ] Email validation (regex + format)
- [ ] Password strength validation (8+ chars, 1 maj, 1 chiffre)
- [ ] Check email not already used
- [ ] Hash password with bcrypt
- [ ] Create user in DB
- [ ] Generate JWT token
- [ ] Send confirmation email
- [ ] Error handling avec messages clairs

## Testing
- POST /api/auth/signup avec credentials valides
- POST avec email already used → 409 error
- POST avec password faible → 400 error
- Email reçu""",
        "labels": ["backend", "auth", "sprint-1", "p0"],
        "assignee": "[Backend Lead]",
        "estimate": "3h",
    },
    {
        "title": "BACK-S1.4 - Implement email confirmation + JWT",
        "body": """## Description
Confirmer email via token JWT, générer auth token.

## Acceptance Criteria
- [ ] POST /api/auth/verify-email implémenté
- [ ] Token verification (signature + expiration)
- [ ] Update user.email_verified = true
- [ ] Generate JWT auth token (7 days)
- [ ] Return token + user info
- [ ] Handle expired/invalid tokens

## Testing
- POST /verify-email avec token valide → 200, auth token
- POST avec token expiré → 401
- Vérifier user.email_verified = true en DB""",
        "labels": ["backend", "auth", "sprint-1", "p0"],
        "assignee": "[Backend Lead]",
        "estimate": "2h",
    },
    {
        "title": "BACK-S1.5 - Implement login controller",
        "body": """## Description
Login : vérifier email/password, retourner auth token.

## Acceptance Criteria
- [ ] POST /api/auth/login implémenté
- [ ] Query user par email
- [ ] Compare password avec bcrypt
- [ ] Generate JWT token (7 days)
- [ ] Return token + user info
- [ ] Rate limiting (prevent brute-force)
- [ ] Error messages génériques (security)

## Testing
- POST /login avec credentials valides → 200, token
- POST avec wrong password → 401
- Brute force (20+ attempts) → 429""",
        "labels": ["backend", "auth", "sprint-1", "p0"],
        "assignee": "[Backend Lead]",
        "estimate": "2h",
    },
    {
        "title": "BACK-S1.6 - Create auth middleware + protected routes",
        "body": """## Description
Middleware JWT verification + route protection.

## Acceptance Criteria
- [ ] authMiddleware.js implémenté
- [ ] GET /api/auth/me (protected)
- [ ] Token extraction from Authorization header
- [ ] Token validation + payload extraction
- [ ] req.userId set
- [ ] 401 si token manquant/invalide

## Testing
- GET /api/auth/me sans token → 401
- GET /api/auth/me avec token valide → 200, user info
- GET /api/auth/me avec token expiré → 401""",
        "labels": ["backend", "auth", "sprint-1", "p0"],
        "assignee": "[Backend Lead]",
        "estimate": "1.5h",
    },
    {
        "title": "BACK-S1.7 - Setup Jest tests + auth test suite",
        "body": """## Description
Créer test setup + tests signup/login/verify.

## Acceptance Criteria
- [ ] jest.config.js configuré
- [ ] Test database setup (test-specific DB)
- [ ] Test helper functions
- [ ] 15+ tests pour signup
- [ ] 10+ tests pour login
- [ ] 10+ tests pour verify-email
- [ ] npm run test = tous tests pass
- [ ] Coverage > 80%

## Testing
- npm test → all pass
- npm test -- --coverage""",
        "labels": ["backend", "testing", "sprint-1", "p1"],
        "assignee": "[Backend Lead]",
        "estimate": "3h",
    },

    # FRONTEND (9)
    {
        "title": "FRONT-S1.1 - Create SignupPage component",
        "body": """## Description
Créer formulaire signup avec validation client-side.

## Acceptance Criteria
- [ ] Form avec inputs : email, username, password, passwordConfirm
- [ ] Client-side validation
- [ ] Submit button (disabled si form invalid)
- [ ] Loading state
- [ ] Error messages affichés
- [ ] Link vers login page
- [ ] TailwindCSS styled (responsive mobile)
- [ ] Accessible

## Testing
- Render component
- Submit invalid email → error shown
- Submit valid form → call API""",
        "labels": ["frontend", "auth", "sprint-1", "p0"],
        "assignee": "[Frontend Lead]",
        "estimate": "2h",
    },
    {
        "title": "FRONT-S1.2 - Create LoginPage component",
        "body": """## Description
Formulaire login avec email/password.

## Acceptance Criteria
- [ ] Form : email + password inputs
- [ ] Submit button
- [ ] Loading state
- [ ] Error messages
- [ ] Link vers signup
- [ ] TailwindCSS styled
- [ ] Accessible

## Testing
- Render component
- Submit credentials
- Error handling""",
        "labels": ["frontend", "auth", "sprint-1", "p0"],
        "assignee": "[Frontend Lead]",
        "estimate": "1.5h",
    },
    {
        "title": "FRONT-S1.3 - Create EmailVerifyPage component",
        "body": """## Description
Page confirmation email avec token extraction.

## Acceptance Criteria
- [ ] Extract token from URL query params
- [ ] Auto-submit verification on mount
- [ ] Loading state
- [ ] Success message (redirect to login)
- [ ] Error handling (expired token, etc.)

## Testing
- Extract token from URL
- Auto-submit on mount
- Redirect to login on success""",
        "labels": ["frontend", "auth", "sprint-1", "p0"],
        "assignee": "[Frontend Lead]",
        "estimate": "1h",
    },
    {
        "title": "FRONT-S1.4 - Setup Zustand auth store",
        "body": """## Description
Global state management pour user + auth tokens.

## Acceptance Criteria
- [ ] useAuthStore hook créé
- [ ] State : user, token, isLoading, error
- [ ] Actions : setUser, setToken, logout, setError
- [ ] Token persisted in localStorage
- [ ] Token retrieved on app load

## Testing
- useAuthStore hook works
- Token persists in localStorage
- Logout clears token""",
        "labels": ["frontend", "state-mgmt", "sprint-1", "p0"],
        "assignee": "[Frontend Lead]",
        "estimate": "1.5h",
    },
    {
        "title": "FRONT-S1.5 - Create PrivateRoute component",
        "body": """## Description
Route wrapper pour pages protégées (require auth).

## Acceptance Criteria
- [ ] Check token exists
- [ ] If no token, redirect to /login
- [ ] If token exists, render component
- [ ] Loading fallback

## Testing
- No token → redirect to /login
- With token → render component""",
        "labels": ["frontend", "routing", "sprint-1", "p1"],
        "assignee": "[Frontend Lead]",
        "estimate": "1h",
    },
    {
        "title": "FRONT-S1.6 - Setup Axios API client + authApi module",
        "body": """## Description
Axios instance + API functions (signup, login, verify).

## Acceptance Criteria
- [ ] axiosInstance.js created
- [ ] Interceptor add Authorization header
- [ ] authApi.js functions : signup, login, verifyEmail
- [ ] Error handling
- [ ] Timeout (30s)

## Testing
- API calls work
- Token in header
- Error handling""",
        "labels": ["frontend", "api", "sprint-1", "p0"],
        "assignee": "[Frontend Lead]",
        "estimate": "2h",
    },
    {
        "title": "FRONT-S1.7 - Error handling + React Hot Toast notifications",
        "body": """## Description
Afficher erreurs + success messages avec toast.

## Acceptance Criteria
- [ ] React Hot Toast provider setup
- [ ] Toast on signup success
- [ ] Toast on signup error
- [ ] Toast on login success
- [ ] Toast on 401 (token expired)
- [ ] Auto-dismiss (5s)
- [ ] Custom styling

## Testing
- Toast appears on success
- Toast appears on error
- Auto-dismisses after 5s""",
        "labels": ["frontend", "ui", "sprint-1", "p1"],
        "assignee": "[Frontend Lead]",
        "estimate": "1.5h",
    },
    {
        "title": "FRONT-S1.8 - Setup React Router + App.jsx",
        "body": """## Description
Routing setup avec pages.

## Acceptance Criteria
- [ ] BrowserRouter setup
- [ ] Routes defined (/, /signup, /login, /verify, /discover, /profile)
- [ ] PrivateRoute wrapper
- [ ] Not found (404) page
- [ ] Navigation working

## Testing
- Routes work
- Navigation between pages
- 404 page shows""",
        "labels": ["frontend", "routing", "sprint-1", "p0"],
        "assignee": "[Frontend Lead]",
        "estimate": "1.5h",
    },
    {
        "title": "FRONT-S1.9 - Component tests + integration tests",
        "body": """## Description
Tests Vitest + React Testing Library.

## Acceptance Criteria
- [ ] SignupPage tests (10+)
- [ ] LoginPage tests (8+)
- [ ] API integration tests
- [ ] PrivateRoute tests
- [ ] Coverage > 70%

## Testing
- npm test → all pass
- Coverage report""",
        "labels": ["frontend", "testing", "sprint-1", "p1"],
        "assignee": "[Frontend Lead]",
        "estimate": "2h",
    },

    # DESIGN (3)
    {
        "title": "DESIGN-S1.1 - Create wireframes (Signup, Login, EmailVerify)",
        "body": """## Description
Wireframes low-fidelity pour pages auth.

## Acceptance Criteria
- [ ] SignupPage wireframe
- [ ] LoginPage wireframe
- [ ] EmailVerifyPage wireframe
- [ ] Mobile layout considered
- [ ] User flow documented

## Tools
Figma, Excalidraw, ou pen & paper""",
        "labels": ["design", "ux", "sprint-1", "p1"],
        "assignee": "[Design/QA]",
        "estimate": "3h",
    },
    {
        "title": "DESIGN-S1.2 - Create UI maquettes (Figma)",
        "body": """## Description
High-fidelity maquettes avec design system.

## Acceptance Criteria
- [ ] Figma file créé (teamfinder-mvp)
- [ ] SignupPage maquette (desktop + mobile)
- [ ] LoginPage maquette
- [ ] EmailVerifyPage maquette
- [ ] Color palette (neon-cyan, neon-purple, gamer-black)
- [ ] Typography (Montserrat, Inter)
- [ ] Buttons, inputs styled
- [ ] Components library started

## Depends On
- DESIGN-S1.1""",
        "labels": ["design", "ui", "sprint-1", "p1"],
        "assignee": "[Design/QA]",
        "estimate": "4h",
    },
    {
        "title": "DESIGN-S1.3 - Create design system documentation",
        "body": """## Description
Document design tokens, components.

## Acceptance Criteria
- [ ] Figma design system created
- [ ] Color tokens documented
- [ ] Typography rules
- [ ] Button styles (primary, secondary, variants)
- [ ] Input styles
- [ ] Spacing system

## Depends On
- DESIGN-S1.2""",
        "labels": ["design", "documentation", "sprint-1", "p2"],
        "assignee": "[Design/QA]",
        "estimate": "2h",
    },
]


def create_issue(issue: Dict) -> bool:
    """Créer une issue sur GitHub"""
    try:
        # Préparer les données
        payload = {
            "title": issue["title"],
            "body": issue["body"],
            "labels": issue.get("labels", []),
        }

        # Créer l'issue
        response = requests.post(
            f"{BASE_URL}/issues",
            headers=HEADERS,
            json=payload
        )

        if response.status_code == 201:
            issue_data = response.json()
            issue_number = issue_data["number"]
            print(f"✅ Issue créée : #{issue_number} - {issue['title']}")
            return True
        else:
            print(f"❌ Erreur : {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Exception : {str(e)}")
        return False


def create_all_issues():
    """Créer toutes les 33 issues"""
    print("🚀 Démarrage de la création des 33 issues...")
    print(f"Repository: {GITHUB_OWNER}/{GITHUB_REPO}")
    print(f"Token: {GITHUB_TOKEN[:20]}..." if GITHUB_TOKEN else "❌ Token not found")
    print("-" * 60)

    created = 0
    failed = 0

    for i, issue in enumerate(ISSUES, 1):
        print(f"\n[{i}/{len(ISSUES)}] Création de : {issue['title']}")
        
        if create_issue(issue):
            created += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(f"📊 Résultats finaux :")
    print(f"✅ Créées : {created}")
    print(f"❌ Échouées : {failed}")
    print(f"📈 Total : {created + failed}/{len(ISSUES)}")
    print("=" * 60)


if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("❌ ERREUR : GITHUB_TOKEN non trouvé dans .env")
        print("Créez un fichier .env avec : GITHUB_TOKEN=ghp_...")
        exit(1)

    create_all_issues()
