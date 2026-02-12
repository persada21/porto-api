"""
GitHub-related API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict

from app.models.schemas import (
    Repository,
    GitHubProfile,
    LanguageStats,
    PortfolioStats,
)
from app.services.github_service import github_service

router = APIRouter()


@router.get("/profile", response_model=GitHubProfile)
async def get_github_profile(username: str):
    """
    Get GitHub user profile information
    
    - **username**: GitHub username
    """
    return await github_service.get_user_profile(username)


@router.get("/repositories", response_model=List[Repository])
async def get_repositories(
    username: str,
    sort: str = Query("updated", regex="^(created|updated|pushed|full_name|stars)$"),
    direction: str = Query("desc", regex="^(asc|desc)$"),
    per_page: int = Query(100, ge=1, le=100),
    page: int = Query(1, ge=1),
    type: str = Query("all", regex="^(all|owner|member)$")
):
    """
    Get all repositories for a GitHub user
    
    - **username**: GitHub username
    - **sort**: Sort by created, updated, pushed, full_name, or stars
    - **direction**: Sort direction (asc or desc)
    - **per_page**: Number of results per page (1-100)
    - **page**: Page number
    - **type**: Filter by all, owner, or member
    """
    return await github_service.get_user_repositories(
        username=username,
        sort=sort,
        direction=direction,
        per_page=per_page,
        page=page,
        repo_type=type
    )


@router.get("/stats", response_model=PortfolioStats)
async def get_portfolio_stats(username: str):
    """
    Get comprehensive portfolio statistics
    
    - **username**: GitHub username
    """
    return await github_service.get_portfolio_stats(username)


@router.get("/languages", response_model=List[LanguageStats])
async def get_languages(username: str):
    """
    Get language statistics for all repositories
    
    - **username**: GitHub username
    """
    stats = await github_service.get_portfolio_stats(username)
    return stats.languages


@router.get("/top-repos")
async def get_top_repositories(
    username: str,
    limit: int = Query(10, ge=1, le=50),
    sort_by: str = Query("stars", regex="^(stars|forks|updated|created)$")
):
    """
    Get top repositories sorted by stars, forks, updated, or created date
    
    - **username**: GitHub username
    - **limit**: Number of repositories to return (1-50)
    - **sort_by**: Sort by stars, forks, updated, or created
    """
    repos_data = await github_service.get_user_repositories(
        username=username,
        sort="updated",
        per_page=100
    )
    
    if not repos_data:
        raise HTTPException(status_code=404, detail="No repositories found")
    
    # Convert to dict for sorting
    repos_dict = [repo.dict() for repo in repos_data]
    
    sort_key_map = {
        "stars": lambda x: x.get("stars", 0),
        "forks": lambda x: x.get("forks", 0),
        "updated": lambda x: x.get("updated_at", ""),
        "created": lambda x: x.get("created_at", "")
    }
    
    sorted_repos = sorted(
        repos_dict,
        key=sort_key_map.get(sort_by, sort_key_map["stars"]),
        reverse=True
    )[:limit]
    
    return [
        {
            "name": repo.get("name", ""),
            "full_name": repo.get("full_name", ""),
            "description": repo.get("description"),
            "url": repo.get("html_url", ""),
            "language": repo.get("language"),
            "stars": repo.get("stars", 0),
            "forks": repo.get("forks", 0),
            "watchers": repo.get("watchers", 0),
            "created_at": repo.get("created_at", ""),
            "updated_at": repo.get("updated_at", ""),
            "topics": repo.get("topics", [])
        }
        for repo in sorted_repos
    ]


@router.get("/recent-repos")
async def get_recent_repositories(
    username: str,
    limit: int = Query(5, ge=1, le=20)
):
    """
    Get recently updated repositories
    
    - **username**: GitHub username
    - **limit**: Number of repositories to return (1-20)
    """
    repos = await github_service.get_user_repositories(
        username=username,
        sort="updated",
        per_page=limit
    )
    
    if not repos:
        raise HTTPException(status_code=404, detail="No repositories found")
    
    repos_dict = [repo.dict() for repo in repos]
    
    return [
        {
            "name": repo.get("name", ""),
            "full_name": repo.get("full_name", ""),
            "description": repo.get("description"),
            "url": repo.get("html_url", ""),
            "language": repo.get("language"),
            "stars": repo.get("stars", 0),
            "forks": repo.get("forks", 0),
            "updated_at": repo.get("pushed_at", ""),
            "topics": repo.get("topics", [])
        }
        for repo in repos_dict
    ]


@router.get("/repository/{repo_name}")
async def get_repository_details(username: str, repo_name: str):
    """
    Get detailed information about a specific repository
    
    - **username**: GitHub username
    - **repo_name**: Repository name
    """
    return await github_service.get_repository_details(username, repo_name)

