# Project Structure

This document explains the FastAPI project structure following best practices.

## Directory Layout

```
fastapi-project/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI app instance and setup
│   │
│   ├── api/                     # API routes
│   │   ├── __init__.py
│   │   └── v1/                  # API version 1
│   │       ├── __init__.py
│   │       ├── api.py           # Router aggregation
│   │       └── endpoints/       # Endpoint modules
│   │           ├── __init__.py
│   │           ├── github.py    # GitHub-related endpoints
│   │           └── health.py    # Health check endpoints
│   │
│   ├── core/                    # Core functionality
│   │   ├── __init__.py
│   │   └── config.py            # Application settings & configuration
│   │
│   ├── models/                  # Data models & schemas
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic models for request/response
│   │
│   └── services/                # Business logic layer
│       ├── __init__.py
│       └── github_service.py    # GitHub API service
│
├── run.py                       # Application entry point
├── main.py                      # Legacy entry point (backward compatibility)
├── requirements.txt              # Python dependencies
├── README.md                    # Project documentation
└── PROJECT_STRUCTURE.md          # This file
```

## Architecture Principles

### 1. Separation of Concerns
- **Models** (`app/models/`): Data structures and validation schemas
- **Services** (`app/services/`): Business logic and external API interactions
- **Endpoints** (`app/api/v1/endpoints/`): HTTP request/response handling
- **Core** (`app/core/`): Configuration and shared utilities

### 2. API Versioning
- All API routes are under `/api/v1/`
- Easy to add `/api/v2/` in the future without breaking changes

### 3. Scalability
- Easy to add new endpoints by creating new files in `endpoints/`
- Service layer can be reused across different endpoints
- Models are centralized and reusable

### 4. Configuration Management
- All settings in `app/core/config.py`
- Environment variables supported via `.env` file
- Type-safe configuration with Pydantic

## File Responsibilities

### `app/main.py`
- Creates FastAPI application instance
- Configures CORS middleware
- Includes API routers
- Root endpoint definition

### `app/core/config.py`
- Application settings
- Environment variable handling
- Configuration defaults

### `app/models/schemas.py`
- Pydantic models for request/response validation
- Type definitions for API contracts

### `app/services/github_service.py`
- GitHub API interactions
- Business logic for data processing
- Error handling for external API calls

### `app/api/v1/endpoints/github.py`
- GitHub-related HTTP endpoints
- Request validation
- Response formatting
- Calls service layer for business logic

### `app/api/v1/endpoints/health.py`
- Health check endpoints
- System status monitoring

### `app/api/v1/api.py`
- Aggregates all endpoint routers
- Defines API version prefix
- Tags for documentation

### `run.py`
- Application entry point
- Starts uvicorn server
- Uses configuration from `app/core/config.py`

## Adding New Features

### To add a new endpoint:

1. Create endpoint file in `app/api/v1/endpoints/`
2. Define router and endpoints
3. Add router to `app/api/v1/api.py`
4. Use existing services or create new ones in `app/services/`

### To add a new service:

1. Create service file in `app/services/`
2. Implement business logic
3. Use in endpoints via dependency injection

### To add a new model:

1. Add schema to `app/models/schemas.py`
2. Export from `app/models/__init__.py`
3. Use in endpoints and services

## Benefits of This Structure

✅ **Maintainability**: Clear separation makes code easy to understand and modify
✅ **Testability**: Services can be tested independently
✅ **Scalability**: Easy to add new features without cluttering
✅ **Reusability**: Services and models can be reused across endpoints
✅ **Type Safety**: Full type hints throughout
✅ **Documentation**: Auto-generated API docs from code structure

