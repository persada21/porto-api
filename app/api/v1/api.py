"""
API v1 router aggregation
"""
from fastapi import APIRouter

from app.api.v1.endpoints import github, health, ai

api_router = APIRouter()

# Include routers
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(
    github.router,
    prefix="/github/{username}",
    tags=["GitHub"]
)
api_router.include_router(
    ai.router,
    prefix="/github/{username}/ai",
    tags=["AI"]
)

