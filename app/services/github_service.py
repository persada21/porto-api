"""
GitHub API service layer
"""
from typing import Optional, Dict, List
import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.models.schemas import (
    Repository,
    GitHubProfile,
    LanguageStats,
    PortfolioStats,
)


class GitHubService:
    """Service for interacting with GitHub API"""
    
    def __init__(self):
        self.base_url = settings.GITHUB_API_BASE
        self.timeout = settings.GITHUB_API_TIMEOUT
        self.headers = {}
        if settings.GITHUB_TOKEN:
            self.headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"
    
    async def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict] = None
    ) -> Dict:
        """Make a request to GitHub API"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}{endpoint}",
                    headers=self.headers,
                    params=params or {},
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise HTTPException(
                        status_code=404, 
                        detail="GitHub user or resource not found"
                    )
                elif e.response.status_code == 403:
                    raise HTTPException(
                        status_code=403, 
                        detail="GitHub API rate limit exceeded. Consider adding GITHUB_TOKEN."
                    )
                raise HTTPException(
                    status_code=500, 
                    detail=f"GitHub API error: {str(e)}"
                )
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=500, 
                    detail=f"Request error: {str(e)}"
                )
    
    async def get_user_profile(self, username: str) -> GitHubProfile:
        """Get GitHub user profile"""
        data = await self._make_request(f"/users/{username}")
        
        return GitHubProfile(
            username=data.get("login", ""),
            name=data.get("name"),
            bio=data.get("bio"),
            avatar_url=data.get("avatar_url", ""),
            html_url=data.get("html_url", ""),
            public_repos=data.get("public_repos", 0),
            public_gists=data.get("public_gists", 0),
            followers=data.get("followers", 0),
            following=data.get("following", 0),
            created_at=data.get("created_at", ""),
            location=data.get("location"),
            blog=data.get("blog"),
            company=data.get("company"),
            twitter_username=data.get("twitter_username")
        )
    
    async def get_user_repositories(
        self,
        username: str,
        sort: str = "updated",
        direction: str = "desc",
        per_page: int = 100,
        page: int = 1,
        repo_type: str = "all"
    ) -> List[Repository]:
        """Get user repositories"""
        params = {
            "sort": sort,
            "direction": direction,
            "per_page": per_page,
            "page": page,
            "type": repo_type
        }
        
        data = await self._make_request(f"/users/{username}/repos", params)
        
        repos = []
        for repo in data:
            repos.append(Repository(
                id=repo.get("id", 0),
                name=repo.get("name", ""),
                full_name=repo.get("full_name", ""),
                description=repo.get("description"),
                url=repo.get("url", ""),
                html_url=repo.get("html_url", ""),
                language=repo.get("language"),
                stars=repo.get("stargazers_count", 0),
                forks=repo.get("forks_count", 0),
                watchers=repo.get("watchers_count", 0),
                open_issues=repo.get("open_issues_count", 0),
                created_at=repo.get("created_at", ""),
                updated_at=repo.get("updated_at", ""),
                pushed_at=repo.get("pushed_at", ""),
                is_fork=repo.get("fork", False),
                is_archived=repo.get("archived", False),
                topics=repo.get("topics", []),
                license=repo.get("license", {}).get("name") if repo.get("license") else None,
                size=repo.get("size", 0),
                default_branch=repo.get("default_branch", "main")
            ))
        
        return repos
    
    async def get_portfolio_stats(self, username: str) -> PortfolioStats:
        """Get comprehensive portfolio statistics"""
        repos_data = await self._make_request(
            f"/users/{username}/repos",
            {"per_page": 100, "sort": "updated"}
        )
        
        if not repos_data:
            raise HTTPException(status_code=404, detail="No repositories found")
        
        total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
        total_forks = sum(repo.get("forks_count", 0) for repo in repos_data)
        total_watchers = sum(repo.get("watchers_count", 0) for repo in repos_data)
        
        # Language statistics
        languages = {}
        language_repos = {}
        
        for repo in repos_data:
            lang = repo.get("language")
            if lang:
                if lang not in languages:
                    languages[lang] = 0
                    language_repos[lang] = []
                languages[lang] += 1
                language_repos[lang].append(repo.get("name", ""))
        
        total_lang_repos = sum(languages.values())
        language_stats = [
            LanguageStats(
                language=lang,
                count=count,
                percentage=round((count / total_lang_repos) * 100, 2) if total_lang_repos > 0 else 0,
                repositories=language_repos[lang]
            )
            for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)
        ]
        
        # Most starred repository
        most_starred = max(repos_data, key=lambda x: x.get("stargazers_count", 0))
        most_starred_repo = {
            "name": most_starred.get("name", ""),
            "stars": most_starred.get("stargazers_count", 0),
            "url": most_starred.get("html_url", ""),
            "description": most_starred.get("description")
        } if repos_data else None
        
        # Recently updated repositories (last 5)
        recent_repos = sorted(
            repos_data,
            key=lambda x: x.get("pushed_at", ""),
            reverse=True
        )[:5]
        
        recently_updated = [
            {
                "name": repo.get("name", ""),
                "updated_at": repo.get("pushed_at", ""),
                "url": repo.get("html_url", ""),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count", 0)
            }
            for repo in recent_repos
        ]
        
        top_languages = [lang.language for lang in language_stats[:5]]
        
        return PortfolioStats(
            total_repositories=len(repos_data),
            total_stars=total_stars,
            total_forks=total_forks,
            total_watchers=total_watchers,
            languages=language_stats,
            most_starred_repo=most_starred_repo,
            recently_updated_repos=recently_updated,
            top_languages=top_languages,
            total_contributions=None
        )
    
    async def get_repository_details(self, username: str, repo_name: str) -> Dict:
        """Get detailed repository information"""
        repo_data = await self._make_request(f"/repos/{username}/{repo_name}")
        languages_data = await self._make_request(f"/repos/{username}/{repo_name}/languages")
        
        return {
            "id": repo_data.get("id"),
            "name": repo_data.get("name", ""),
            "full_name": repo_data.get("full_name", ""),
            "description": repo_data.get("description"),
            "url": repo_data.get("html_url", ""),
            "language": repo_data.get("language"),
            "languages": languages_data,
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "watchers": repo_data.get("watchers_count", 0),
            "open_issues": repo_data.get("open_issues_count", 0),
            "created_at": repo_data.get("created_at", ""),
            "updated_at": repo_data.get("updated_at", ""),
            "pushed_at": repo_data.get("pushed_at", ""),
            "is_fork": repo_data.get("fork", False),
            "is_archived": repo_data.get("archived", False),
            "is_private": repo_data.get("private", False),
            "topics": repo_data.get("topics", []),
            "license": repo_data.get("license", {}).get("name") if repo_data.get("license") else None,
            "size": repo_data.get("size", 0),
            "default_branch": repo_data.get("default_branch", "main"),
            "homepage": repo_data.get("homepage"),
            "has_wiki": repo_data.get("has_wiki", False),
            "has_pages": repo_data.get("has_pages", False),
            "has_issues": repo_data.get("has_issues", True),
            "has_projects": repo_data.get("has_projects", False)
        }

    async def get_user_events(self, username: str, limit: int = 30) -> List[Dict]:
        """Get user public events"""
        params = {"per_page": limit}
        events = await self._make_request(f"/users/{username}/events/public", params)
        return events

    async def get_readme_content(self, username: str, repo_name: str) -> Optional[str]:
        """Get repository README content"""
        try:
            # Using raw media type header to get content directly
            headers = self.headers.copy()
            headers["Accept"] = "application/vnd.github.raw"

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{username}/{repo_name}/readme",
                    headers=headers,
                    timeout=self.timeout
                )
                if response.status_code == 200:
                    return response.text
                return None
        except Exception:
            return None


# Create service instance
github_service = GitHubService()

