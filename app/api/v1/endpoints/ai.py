"""
AI related endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.services.github_service import github_service
from app.services.ai_service import ai_service
from app.models.schemas import AIPersonaResponse, AICommitResponse

router = APIRouter()

@router.get("/persona", response_model=AIPersonaResponse)
async def get_persona(
    username: str,
    limit: int = Query(30, ge=10, le=100)
):
    """
    Analyze developer persona based on recent commit messages.
    """
    events = await github_service.get_user_events(username, limit=limit)
    return ai_service.analyze_persona(events)

@router.get("/generate-commit", response_model=AICommitResponse)
async def generate_commit(
    username: str,
    limit: int = Query(50, ge=10, le=100)
):
    """
    Generate a new commit message in the style of the user.
    """
    events = await github_service.get_user_events(username, limit=limit)
    message = ai_service.generate_commit_message(events)

    # Count source commits
    commits_count = len(ai_service._extract_commits(events))

    return AICommitResponse(
        generated_message=message,
        source_commits_count=commits_count
    )
