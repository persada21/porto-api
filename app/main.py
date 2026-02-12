"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🚀 GitHub Portfolio API - Showcase Your Amazing GitHub Profile!",
        "version": settings.API_VERSION,
        "endpoints": {
            "profile": "/api/v1/github/{username}/profile",
            "repositories": "/api/v1/github/{username}/repositories",
            "stats": "/api/v1/github/{username}/stats",
            "languages": "/api/v1/github/{username}/languages",
            "top-repos": "/api/v1/github/{username}/top-repos",
            "recent-repos": "/api/v1/github/{username}/recent-repos",
            "repository": "/api/v1/github/{username}/repository/{repo_name}"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }

