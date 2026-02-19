"""
Pydantic schemas for request/response models
"""
from pydantic import BaseModel
from typing import Optional, List, Dict


class Repository(BaseModel):
    """Repository schema"""
    id: int
    name: str
    full_name: str
    description: Optional[str]
    url: str
    html_url: str
    language: Optional[str]
    stars: int
    forks: int
    watchers: int
    open_issues: int
    created_at: str
    updated_at: str
    pushed_at: str
    is_fork: bool
    is_archived: bool
    topics: List[str]
    license: Optional[str]
    size: int
    default_branch: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 123456789,
                "name": "awesome-project",
                "full_name": "username/awesome-project",
                "description": "An awesome project",
                "url": "https://api.github.com/repos/username/awesome-project",
                "html_url": "https://github.com/username/awesome-project",
                "language": "Python",
                "stars": 100,
                "forks": 20,
                "watchers": 50,
                "open_issues": 5,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-12-01T00:00:00Z",
                "pushed_at": "2023-12-01T00:00:00Z",
                "is_fork": False,
                "is_archived": False,
                "topics": ["python", "api"],
                "license": "MIT",
                "size": 1024,
                "default_branch": "main"
            }
        }


class GitHubProfile(BaseModel):
    """GitHub user profile schema"""
    username: str
    name: Optional[str]
    bio: Optional[str]
    avatar_url: str
    html_url: str
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: str
    location: Optional[str]
    blog: Optional[str]
    company: Optional[str]
    twitter_username: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "username": "octocat",
                "name": "The Octocat",
                "bio": "GitHub's mascot",
                "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                "html_url": "https://github.com/octocat",
                "public_repos": 8,
                "public_gists": 8,
                "followers": 3000,
                "following": 9,
                "created_at": "2011-01-25T18:44:36Z",
                "location": "San Francisco",
                "blog": "https://github.blog",
                "company": "GitHub",
                "twitter_username": "github"
            }
        }


class LanguageStats(BaseModel):
    """Language statistics schema"""
    language: str
    count: int
    percentage: float
    repositories: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "language": "Python",
                "count": 10,
                "percentage": 50.0,
                "repositories": ["repo1", "repo2"]
            }
        }


class PortfolioStats(BaseModel):
    """Portfolio statistics schema"""
    total_repositories: int
    total_stars: int
    total_forks: int
    total_watchers: int
    languages: List[LanguageStats]
    most_starred_repo: Optional[Dict]
    recently_updated_repos: List[Dict]
    top_languages: List[str]
    total_contributions: Optional[int]

    class Config:
        json_schema_extra = {
            "example": {
                "total_repositories": 20,
                "total_stars": 500,
                "total_forks": 100,
                "total_watchers": 200,
                "languages": [],
                "most_starred_repo": {"name": "awesome-repo", "stars": 100},
                "recently_updated_repos": [],
                "top_languages": ["Python", "JavaScript"],
                "total_contributions": None
            }
        }


class ContributionStats(BaseModel):
    """Contribution statistics schema"""
    total_contributions: int
    contributions_by_year: Dict[str, int]
    contributions_by_month: Dict[str, int]
    streak_days: Optional[int]
    longest_streak_days: Optional[int]


class AIPersonaResponse(BaseModel):
    """AI Persona analysis response"""
    persona: str
    vibe: str
    traits: List[str]
    commit_distribution: Dict[str, int]

    class Config:
        json_schema_extra = {
            "example": {
                "persona": "The Creator",
                "vibe": "Always building something new. A true innovator.",
                "traits": ["Prolific", "Balanced"],
                "commit_distribution": {"feat": 10, "fix": 2, "other": 1}
            }
        }


class AICommitResponse(BaseModel):
    """AI Generated commit response"""
    generated_message: str
    source_commits_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "generated_message": "feat: add new endpoint for user data",
                "source_commits_count": 50
            }
        }


class RAGQueryRequest(BaseModel):
    """RAG Query Request schema"""
    query: str

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What technologies does this user work with?"
            }
        }


class RAGResponse(BaseModel):
    """RAG Response schema"""
    answer: str
    sources: List[str]
    context_used: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "The user works primarily with Python and FastAPI...",
                "sources": ["fastapi-project", "another-repo"],
                "context_used": ["Repository: fastapi-project...", "README for..."]
            }
        }
