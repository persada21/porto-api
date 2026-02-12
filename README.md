# 🚀 GitHub Portfolio API

An amazing FastAPI application to showcase your GitHub profile and repositories. Built with best practices and a clean, scalable architecture.

## ✨ Features

- **Clean Architecture** - Well-organized folder structure following FastAPI best practices
- **GitHub Profile Information** - Get detailed profile data
- **Repository Statistics** - Comprehensive stats about all your repositories
- **Language Analytics** - See which programming languages you use most
- **Top Repositories** - Find your most starred and popular repos
- **Recent Activity** - Track your latest repository updates
- **Detailed Repository Info** - Get in-depth information about specific repos
- **Automatic API Documentation** - Interactive Swagger UI and ReDoc
- **CORS Enabled** - Ready for frontend integration
- **Environment Configuration** - Easy configuration via environment variables

## 📁 Project Structure

```
fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py          # API router aggregation
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── github.py   # GitHub endpoints
│   │           └── health.py   # Health check endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Application configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models/schemas
│   └── services/
│       ├── __init__.py
│       └── github_service.py   # GitHub API service layer
├── run.py                      # Application runner
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .env.example               # Environment variables example
```

## 🛠️ Installation

1. **Clone or navigate to the project:**
```bash
cd fastapi-project
```

2. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables (optional):**
```bash
cp .env.example .env
# Edit .env and add your GITHUB_TOKEN if needed
```

> **Note:** Without a token, you're limited to 60 requests/hour. With a token, you get 5,000 requests/hour.

## 🚀 Running the Application

### Development Mode (with auto-reload):
```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload
```

The application will be available at:
- **API**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## 📚 API Endpoints

### Base Endpoints

- `GET /` - API information and available endpoints
- `GET /api/v1/health` - Health check endpoint

### GitHub Profile Endpoints

All GitHub endpoints are prefixed with `/api/v1/github/{username}`

#### Get User Profile
```http
GET /api/v1/github/{username}/profile
```

**Example:**
```bash
curl http://localhost:8000/api/v1/github/octocat/profile
```

#### Get All Repositories
```http
GET /api/v1/github/{username}/repositories
```

**Query Parameters:**
- `sort` - Sort by: `created`, `updated`, `pushed`, `full_name`, `stars` (default: `updated`)
- `direction` - Sort direction: `asc` or `desc` (default: `desc`)
- `per_page` - Results per page: 1-100 (default: 100)
- `page` - Page number (default: 1)
- `type` - Filter: `all`, `owner`, `member` (default: `all`)

**Example:**
```bash
curl "http://localhost:8000/api/v1/github/octocat/repositories?sort=stars&per_page=10"
```

#### Get Portfolio Statistics
```http
GET /api/v1/github/{username}/stats
```

**Example:**
```bash
curl http://localhost:8000/api/v1/github/octocat/stats
```

**Response includes:**
- Total repositories, stars, forks, watchers
- Language statistics with percentages
- Most starred repository
- Recently updated repositories
- Top languages

#### Get Language Statistics
```http
GET /api/v1/github/{username}/languages
```

**Example:**
```bash
curl http://localhost:8000/api/v1/github/octocat/languages
```

#### Get Top Repositories
```http
GET /api/v1/github/{username}/top-repos
```

**Query Parameters:**
- `limit` - Number of repos to return: 1-50 (default: 10)
- `sort_by` - Sort by: `stars`, `forks`, `updated`, `created` (default: `stars`)

**Example:**
```bash
curl "http://localhost:8000/api/v1/github/octocat/top-repos?limit=5&sort_by=stars"
```

#### Get Recent Repositories
```http
GET /api/v1/github/{username}/recent-repos
```

**Query Parameters:**
- `limit` - Number of repos: 1-20 (default: 5)

**Example:**
```bash
curl "http://localhost:8000/api/v1/github/octocat/recent-repos?limit=10"
```

#### Get Repository Details
```http
GET /api/v1/github/{username}/repository/{repo_name}
```

**Example:**
```bash
curl http://localhost:8000/api/v1/github/octocat/Hello-World/repository
```

## 💡 Usage Examples

### Get Your Own Portfolio Stats
```bash
# Replace 'your-username' with your GitHub username
curl http://localhost:8000/api/v1/github/your-username/stats
```

### Find Your Most Starred Repositories
```bash
curl "http://localhost:8000/api/v1/github/your-username/top-repos?limit=5&sort_by=stars"
```

### See Your Language Distribution
```bash
curl http://localhost:8000/api/v1/github/your-username/languages
```

### Get Your Profile Information
```bash
curl http://localhost:8000/api/v1/github/your-username/profile
```

## 🎯 Use Cases

- **Portfolio Websites** - Display your GitHub stats on your personal website
- **Resume Enhancement** - Showcase your coding activity and languages
- **Job Applications** - Provide a quick overview of your GitHub profile
- **Analytics Dashboard** - Track your repository statistics over time
- **Social Sharing** - Share your GitHub achievements

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# GitHub API Token (optional but recommended)
GITHUB_TOKEN=your_github_token_here

# Server Configuration (optional)
HOST=0.0.0.0
PORT=8000
RELOAD=true
```

- `GITHUB_TOKEN` - Optional GitHub personal access token for higher rate limits
  - Create one at: https://github.com/settings/tokens
  - No special permissions needed (public repo access is enough)

### Rate Limits

- **Without token**: 60 requests/hour per IP
- **With token**: 5,000 requests/hour

## 🏗️ Architecture

This project follows FastAPI best practices:

- **Separation of Concerns**: Models, services, and endpoints are separated
- **API Versioning**: Routes are versioned (`/api/v1/`)
- **Service Layer**: Business logic is in services, not endpoints
- **Configuration Management**: Centralized config using Pydantic Settings
- **Type Safety**: Full type hints and Pydantic models
- **Scalability**: Easy to add new endpoints and features

## 🚀 Deployment

### Deploy to Heroku

1. Create a `Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Deploy:
```bash
heroku create your-app-name
heroku config:set GITHUB_TOKEN=your_token
git push heroku main
```

### Deploy to Railway/Render

Similar process - set the `GITHUB_TOKEN` environment variable and deploy!

## 🐛 Error Handling

The API handles common errors:
- **404**: User or repository not found
- **403**: Rate limit exceeded (add GITHUB_TOKEN)
- **500**: Server or GitHub API errors

## 📝 License

MIT

## 🤝 Contributing

Feel free to fork, improve, and create pull requests!

## ⭐ Show Your Support

If you find this API useful, star it on GitHub!

---

**Made with ❤️ using FastAPI**
