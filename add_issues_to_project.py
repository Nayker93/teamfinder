#!/usr/bin/env python3
"""
Script pour ajouter les 33 issues au GitHub Project Board
VERSION CORRIGÉE - Utilise REST API + GraphQL
"""

import requests
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_PROJECT_NUMBER = int(os.getenv("GITHUB_PROJECT_NUMBER", "1"))

# API endpoints
REST_BASE_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
GRAPHQL_URL = "https://api.github.com/graphql"  # CORRIGÉ : api.github.com au lieu de api.graphql.github.com

# Headers corrects pour REST et GraphQL
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",  # Format correct (pas "Bearer")
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

print("=" * 70)
print("🔧 DEBUG INFO")
print("=" * 70)
print(f"✅ GITHUB_OWNER: {GITHUB_OWNER}")
print(f"✅ GITHUB_REPO: {GITHUB_REPO}")
print(f"✅ PROJECT_NUMBER: {GITHUB_PROJECT_NUMBER}")
print(f"✅ GRAPHQL_URL: {GRAPHQL_URL}")
print(f"✅ TOKEN (first 20 chars): {GITHUB_TOKEN[:20] if GITHUB_TOKEN else '❌ NOT FOUND'}...")
print("=" * 70)


# ===== GRAPHQL QUERIES =====

GET_PROJECT_ID_QUERY = """
query($owner:String!, $number:Int!) {
  repository(owner: $owner, name: "teamfinder") {
    projectV2(number: $number) {
      id
      title
      number
    }
  }
}
"""

GET_ISSUES_QUERY = """
query($owner:String!, $repo:String!) {
  repository(owner: $owner, name: $repo) {
    issues(first: 100, states: OPEN) {
      nodes {
        id
        number
        title
      }
      pageInfo {
        hasNextPage
      }
    }
  }
}
"""

ADD_TO_PROJECT_QUERY = """
mutation($projectId:ID!, $contentId:ID!) {
  addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
    item {
      id
    }
  }
}
"""


def make_graphql_request(query, variables):
    """Faire une requête GraphQL"""
    try:
        payload = {
            "query": query,
            "variables": variables
        }
        
        print(f"📡 GraphQL Request: {variables}")
        
        response = requests.post(
            GRAPHQL_URL,
            headers=HEADERS,
            json=payload,
            timeout=10
        )
        
        print(f"   Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Vérifier les erreurs GraphQL
            if "errors" in data:
                print(f"   ❌ GraphQL Error: {data['errors']}")
                return None
            
            return data.get("data")
        else:
            print(f"   ❌ HTTP Error {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
    
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return None


def get_project_id():
    """Récupérer l'ID du project"""
    print("\n📍 Récupération du Project ID...")
    
    variables = {
        "owner": GITHUB_OWNER,
        "number": GITHUB_PROJECT_NUMBER
    }
    
    data = make_graphql_request(GET_PROJECT_ID_QUERY, variables)
    
    if data:
        try:
            project = data["repository"]["projectV2"]
            if project:
                project_id = project["id"]
                project_title = project["title"]
                print(f"   ✅ Project trouvé: {project_title}")
                print(f"   ✅ Project ID: {project_id[:30]}...")
                return project_id
        except Exception as e:
            print(f"   ❌ Error parsing project data: {e}")
            print(f"   Data received: {data}")
    
    print("   ❌ Project non trouvé")
    return None


def get_issues():
    """Récupérer toutes les issues du repo"""
    print("\n📋 Récupération des issues...")
    
    variables = {
        "owner": GITHUB_OWNER,
        "repo": GITHUB_REPO
    }
    
    data = make_graphql_request(GET_ISSUES_QUERY, variables)
    
    if data:
        try:
            issues = data["repository"]["issues"]["nodes"]
            print(f"   ✅ {len(issues)} issues trouvées")
            return issues
        except Exception as e:
            print(f"   ❌ Error parsing issues data: {e}")
            print(f"   Data received: {data}")
    
    print("   ❌ Aucune issue trouvée")
    return []


def add_issue_to_project(project_id, issue_id, issue_number, issue_title):
    """Ajouter une issue au project"""
    
    variables = {
        "projectId": project_id,
        "contentId": issue_id
    }
    
    data = make_graphql_request(ADD_TO_PROJECT_QUERY, variables)
    
    if data and "addProjectV2ItemById" in data:
        item = data["addProjectV2ItemById"]["item"]
        if item:
            print(f"   ✅ Issue #{issue_number} ajoutée au project")
            return True
    
    print(f"   ❌ Erreur: Issue #{issue_number} non ajoutée")
    return False


def add_all_issues_to_project():
    """Ajouter toutes les issues au project"""
    print("\n" + "=" * 70)
    print("🚀 Démarrage de l'ajout des issues au Project Board...")
    print("=" * 70)
    print(f"Repository: {GITHUB_OWNER}/{GITHUB_REPO}")
    print(f"Project Number: #{GITHUB_PROJECT_NUMBER}")
    print("=" * 70)
    
    # Étape 1: Récupérer le project ID
    project_id = get_project_id()
    if not project_id:
        print("\n❌ Impossible de récupérer le Project ID")
        return False
    
    # Étape 2: Récupérer les issues
    issues = get_issues()
    if not issues:
        print("\n❌ Aucune issue trouvée")
        return False
    
    # Étape 3: Ajouter chaque issue au project
    print(f"\n➕ Ajout de {len(issues)} issues au project...")
    print("-" * 70)
    
    added = 0
    failed = 0
    
    for i, issue in enumerate(issues, 1):
        issue_id = issue["id"]
        issue_number = issue["number"]
        issue_title = issue["title"]
        
        print(f"\n[{i}/{len(issues)}] Issue #{issue_number}: {issue_title[:50]}...")
        
        if add_issue_to_project(project_id, issue_id, issue_number, issue_title):
            added += 1
        else:
            failed += 1
        
        # Rate limiting : attendre 200ms entre chaque requête
        time.sleep(0.2)
    
    print("\n" + "=" * 70)
    print(f"📊 Résultats finaux:")
    print(f"✅ Ajoutées: {added}/{len(issues)}")
    print(f"❌ Échouées: {failed}/{len(issues)}")
    print("=" * 70)
    
    if added == len(issues):
        print("\n✨ Succès ! Toutes les issues ont été ajoutées au project!")
        print("🔄 Allez sur GitHub Projects pour voir les issues")
        return True
    else:
        print(f"\n⚠️ {failed} issues n'ont pas pu être ajoutées")
        print("Vérifiez les messages d'erreur ci-dessus")
        return False


if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("❌ ERREUR: GITHUB_TOKEN non trouvé dans .env")
        exit(1)
    
    if not GITHUB_OWNER or not GITHUB_REPO:
        print("❌ ERREUR: GITHUB_OWNER ou GITHUB_REPO non trouvé dans .env")
        exit(1)
    
    success = add_all_issues_to_project()
    exit(0 if success else 1)