"""
Example usage script for GitHub Portfolio API
Run this after starting the server with: python main.py
"""

import httpx
import json

BASE_URL = "http://localhost:8000"

def print_json(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))

def main():
    # Replace with your GitHub username
    username = "octocat"  # Change this to your username
    
    print(f"🚀 GitHub Portfolio API Examples for: {username}\n")
    print("=" * 60)
    
    # 1. Get profile
    print("\n1️⃣  Getting GitHub Profile...")
    print("-" * 60)
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/api/github/{username}/profile")
        if response.status_code == 200:
            print_json(response.json())
    
    # 2. Get portfolio stats
    print("\n2️⃣  Getting Portfolio Statistics...")
    print("-" * 60)
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/api/github/{username}/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"Total Repositories: {stats['total_repositories']}")
            print(f"Total Stars: {stats['total_stars']}")
            print(f"Total Forks: {stats['total_forks']}")
            print(f"\nTop Languages:")
            for lang in stats['top_languages']:
                print(f"  - {lang}")
            if stats['most_starred_repo']:
                print(f"\nMost Starred Repo: {stats['most_starred_repo']['name']} ({stats['most_starred_repo']['stars']} stars)")
    
    # 3. Get top repositories
    print("\n3️⃣  Getting Top 5 Repositories by Stars...")
    print("-" * 60)
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/api/github/{username}/top-repos?limit=5&sort_by=stars")
        if response.status_code == 200:
            repos = response.json()
            for i, repo in enumerate(repos, 1):
                print(f"{i}. {repo['name']} - ⭐ {repo['stars']} stars - {repo['language'] or 'N/A'}")
    
    # 4. Get language statistics
    print("\n4️⃣  Getting Language Statistics...")
    print("-" * 60)
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/api/github/{username}/languages")
        if response.status_code == 200:
            languages = response.json()
            for lang in languages[:5]:  # Top 5
                print(f"{lang['language']}: {lang['count']} repos ({lang['percentage']}%)")
    
    # 5. Get recent repositories
    print("\n5️⃣  Getting Recent Repositories...")
    print("-" * 60)
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/api/github/{username}/recent-repos?limit=5")
        if response.status_code == 200:
            repos = response.json()
            for repo in repos:
                print(f"📦 {repo['name']} - Updated: {repo['updated_at'][:10]}")

if __name__ == "__main__":
    print("\n⚠️  Make sure the API server is running!")
    print("Start it with: python main.py\n")
    input("Press Enter to continue...")
    main()

