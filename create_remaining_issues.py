#!/usr/bin/env python3
"""
Script pour créer les issues restantes (DESIGN-S1 + Sprint 2)
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")

BASE_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

# 🎯 LES 9 ISSUES RESTANTES
ISSUES = [
    # DESIGN SPRINT 1 (3)
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
Figma, Excalidraw, ou pen & paper

## Testing
- Wireframes reviewed by team
- User flows documented

## Resources
- https://www.figma.com (free account)
- https://excalidraw.com (online tool)""",
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
- [ ] LoginPage maquette (desktop + mobile)
- [ ] EmailVerifyPage maquette
- [ ] Color palette (neon-cyan, neon-purple, gamer-black)
- [ ] Typography (Montserrat, Inter)
- [ ] Buttons, inputs styled
- [ ] Components library started

## Depends On
- DESIGN-S1.1

## Resources
- Figma Pro (free tier ok)
- https://www.figma.com/design""",
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
- [ ] Color tokens documented (names, hex values)
- [ ] Typography rules (fonts, sizes, weights)
- [ ] Button styles (primary, secondary, variants)
- [ ] Input styles (text, email, password)
- [ ] Spacing system (4, 8, 16, 24, 32px)
- [ ] Component naming conventions
- [ ] Accessibility guidelines

## Depends On
- DESIGN-S1.2

## Resources
- Design System Best Practices
- https://bradfrost.com/blog/post/atomic-web-design/""",
        "labels": ["design", "documentation", "sprint-1", "p2"],
        "assignee": "[Design/QA]",
        "estimate": "2h",
    },

    # OPTIONNEL : SPRINT 2 - Profil Multi-Jeux (si vous voulez)
    {
        "title": "BACK-S2.1 - Add game to user profile endpoint",
        "body": """## Description
Créer endpoint pour ajouter un jeu au profil utilisateur.

## Acceptance Criteria
- [ ] POST /api/user/games endpoint créé
- [ ] Accept : user_id, game_id, rank, role
- [ ] Validate game exists
- [ ] Check user not already has this game
- [ ] Return created game with user_games info
- [ ] Error handling (400, 409)

## Testing
- POST avec game_id valide → 201 created
- POST avec game already added → 409 conflict
- Missing required fields → 400 bad request

## Depends On
- BACK-S1.7 (tests setup)""",
        "labels": ["backend", "profile", "sprint-2", "p0"],
        "assignee": "[Backend Lead]",
        "estimate": "1.5h",
    },
    {
        "title": "BACK-S2.2 - Edit game ranking endpoint",
        "body": """## Description
Créer endpoint pour éditer le rang et rôle d'un jeu.

## Acceptance Criteria
- [ ] PUT /api/user/games/:gameId endpoint
- [ ] Update rank, role fields
- [ ] Validate game_id exists for user
- [ ] Return updated user_games entry
- [ ] Error handling

## Testing
- PUT avec données valides → 200 updated
- PUT avec game not found → 404
- PUT avec game not in user profile → 404""",
        "labels": ["backend", "profile", "sprint-2", "p0"],
        "assignee": "[Backend Lead]",
        "estimate": "1h",
    },
    {
        "title": "FRONT-S2.1 - Create ProfileSetupPage component",
        "body": """## Description
Page pour ajouter et gérer les jeux de l'utilisateur.

## Acceptance Criteria
- [ ] Display user info (email, username, avatar)
- [ ] Game selector (dropdown or search)
- [ ] Rank selector (game-specific options)
- [ ] Role selector (game-specific options)
- [ ] Add game button (max 5 games)
- [ ] List existing games
- [ ] Edit/Delete buttons per game
- [ ] TailwindCSS styled

## Testing
- Render without errors
- Add game flow works
- Edit game flow works
- Delete game works
- Max 5 games enforced""",
        "labels": ["frontend", "profile", "sprint-2", "p0"],
        "assignee": "[Frontend Lead]",
        "estimate": "2h",
    },
    {
        "title": "FRONT-S2.2 - Create GameForm component",
        "body": """## Description
Formulaire pour ajouter/éditer un jeu dans le profil.

## Acceptance Criteria
- [ ] Game selector (autocomplete)
- [ ] Rank dropdown (game-specific)
- [ ] Role dropdown (game-specific)
- [ ] Playstyle selection (optional)
- [ ] Form validation
- [ ] Submit/Cancel buttons
- [ ] Loading state

## Testing
- Form renders correctly
- Validation works
- Submit calls API correctly""",
        "labels": ["frontend", "forms", "sprint-2", "p0"],
        "assignee": "[Frontend Lead]",
        "estimate": "1.5h",
    },
    {
        "title": "BACK-S2.3 - Implement matching algorithm",
        "body": """## Description
Créer l'algorithme de matching entre utilisateurs.

## Acceptance Criteria
- [ ] Find candidates for user (same games, similar ranks)
- [ ] Calculate match score (0-100)
- [ ] Exclude : user self, already interacted, blocked
- [ ] Return ordered by score (highest first)
- [ ] Pagination support (20 results)

## Algorithm
Score = (game_match * 40) + (rank_similarity * 40) + (playstyle * 20)

## Testing
- Algorithm returns correct candidates
- Score calculation accurate
- Self exclusion works
- Already liked exclusion works""",
        "labels": ["backend", "matching", "sprint-2", "p0"],
        "assignee": "[Backend Lead]",
        "estimate": "4h",
    },
    {
        "title": "BACK-S2.4 - Get candidates endpoint",
        "body": """## Description
Endpoint pour récupérer les profils compatibles.

## Acceptance Criteria
- [ ] GET /api/match/candidates endpoint
- [ ] Filter by game_id (query param)
- [ ] Return list of candidates (max 20)
- [ ] Each candidate: id, username, avatar, games, rank, score
- [ ] Pagination (offset/limit)
- [ ] Auth required

## Testing
- GET without auth → 401
- GET with game_id → correct candidates
- GET without game_id → all candidates
- Pagination works""",
        "labels": ["backend", "matching", "sprint-2", "p0"],
        "assignee": "[Backend Lead]",
        "estimate": "1.5h",
    },
]


def create_issue(issue):
    """Créer une issue sur GitHub"""
    try:
        payload = {
            "title": issue["title"],
            "body": issue["body"],
            "labels": issue.get("labels", []),
        }

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
            print(f"❌ Erreur : {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Exception : {str(e)}")
        return False


def create_all_remaining_issues():
    """Créer toutes les issues restantes"""
    print("🚀 Démarrage de la création des issues restantes...")
    print(f"Repository: {GITHUB_OWNER}/{GITHUB_REPO}")
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
        exit(1)

    create_all_remaining_issues()
