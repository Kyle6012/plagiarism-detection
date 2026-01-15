# Developer Guide: Plagiarism & AI Detection System

## Getting Started

This guide provides instructions for setting up the development environment and contributing to the project.

## New Features Overview

The system has been enhanced with:
- **Role-based Access Control**: Admin, moderator, and user roles
- **User Management**: Admin panel for managing users
- **Database Seeding**: Automatic setup of initial data
- **Enhanced Security**: Improved authentication and authorization
- **Multi-user Support**: Full support for multiple concurrent users

## Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- Docker and Docker Compose
- Git
- Poetry (for backend dependency management)

## Setting Up Development Environment

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

4. Create a development environment file:
```bash
cp .env.docker.example .env.docker
# Edit .env.docker with your development settings
```

5. Run the backend locally:
```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Project Structure

### Backend Structure
```
backend/
├── app/
│   ├── api/              # API routes and controllers
│   │   ├── v1/           # Version 1 API endpoints
│   │   └── auth.py       # Authentication endpoints
│   ├── core/             # Core application logic
│   │   ├── config.py     # Configuration settings
│   │   ├── db.py         # Database connections
│   │   └── celery.py     # Task queue configuration
│   ├── models/           # SQLAlchemy database models
│   ├── services/         # Business logic implementations
│   │   ├── ai_detection.py    # AI detection logic
│   │   ├── embedding.py       # Text embedding services
│   │   ├── plagiarism.py      # Plagiarism detection logic
│   │   ├── batch_processing.py # Batch processing services
│   │   └── ...               # Other services
│   ├── main.py           # Application entry point
│   └── schemas.py        # Pydantic schemas
├── requirements.txt      # Python dependencies
└── pyproject.toml        # Poetry configuration
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/       # React components
│   │   ├── AIDetectionPage.tsx    # AI detection UI
│   │   ├── UploadForm.tsx         # File upload component
│   │   └── ...                   # Other components
│   ├── contexts/         # React contexts
│   ├── hooks/           # Custom React hooks
│   ├── App.tsx          # Main application component
│   └── main.tsx         # Entry point
├── package.json         # Node.js dependencies
├── vite.config.ts       # Vite configuration
└── tailwind.config.js   # Tailwind CSS configuration
```

## Development Workflow

### Adding New Features

1. Create a new branch:
```bash
git checkout -b feature/new-feature-name
```

2. Develop your feature in the appropriate directory
3. Write tests for your new functionality
4. Update documentation if needed
5. Commit your changes:
```bash
git add .
git commit -m "Add new feature: description of changes"
```

6. Push and create a pull request:
```bash
git push origin feature/new-feature-name
```

### Backend Development

#### Creating New API Endpoints

1. Define the endpoint in the appropriate router file:
```python
# In app/api/v1/routes.py
@router.get("/new-endpoint")
async def new_endpoint():
    return {"message": "Hello World"}
```

2. Create Pydantic models for request/response validation:
```python
from pydantic import BaseModel

class NewRequest(BaseModel):
    param1: str
    param2: int
```

3. Add authentication if required:
```python
from app.api.auth import fastapi_users, admin_user, mod_or_admin_user

# For regular authenticated users
@router.get("/protected-endpoint")
async def protected_endpoint(
    user: User = Depends(fastapi_users.current_user())
):
    return {"user": user.email}

# For admin users only
@router.get("/admin-endpoint")
async def admin_endpoint(
    user: User = Depends(admin_user)
):
    return {"admin": user.email}

# For moderators or admins
@router.get("/mod-endpoint")
async def mod_endpoint(
    user: User = Depends(mod_or_admin_user)
):
    return {"moderator": user.email}
```

4. Create new admin endpoints in the admin API module:
```python
# In app/api/admin.py
@router.get("/admin/custom-action")
async def custom_admin_action(
    current_user: User = Depends(admin_user),
    db: AsyncSession = Depends(get_db)
):
    # Admin-only functionality
    return {"message": "Success"}
```
#### Creating New Services

1. Create a new service file in `app/services/`
2. Implement the business logic with proper error handling
3. Use dependency injection where appropriate
4. Add type hints for better code quality

### Frontend Development

#### Creating New Components

1. Create a new component file in `src/components/`
2. Use TypeScript interfaces for props:
```tsx
interface MyComponentProps {
    title: string;
    items: string[];
}
```

3. Follow the existing design system patterns
4. Handle loading and error states appropriately

#### API Integration

1. Use the existing authentication pattern:
```tsx
const token = localStorage.getItem('token');
const response = await fetch('/api/endpoint', {
    headers: { 'Authorization': `Bearer ${token}` }
});
```

2. Implement proper error handling:
```tsx
try {
    const response = await fetch('/api/endpoint');
    if (!response.ok) throw new Error('Request failed');
    const data = await response.json();
} catch (error) {
    console.error(error);
    // Handle error appropriately
}
```

## Testing

### Backend Testing

Run all backend tests:
```bash
cd backend
poetry run pytest
```

Run specific test file:
```bash
poetry run pytest tests/test_specific_file.py
```

Run tests with coverage:
```bash
poetry run pytest --cov=app
```

### Frontend Testing

Run frontend tests:
```bash
cd frontend
npm test
```

## Code Quality

### Python Code Standards

- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for public functions
- Keep functions focused and small
- Use meaningful variable names

### JavaScript/TypeScript Standards

- Use TypeScript for type safety
- Follow React best practices
- Use consistent naming conventions
- Keep components focused and reusable
- Handle asynchronous operations properly

## Database Migrations

### Using Alembic

1. Make changes to models in `app/models/`
2. Generate migration:
```bash
cd backend
poetry run alembic revision --autogenerate -m "Description of changes"
```

3. Apply migration:
```bash
poetry run alembic upgrade head
```

## Environment Variables

Development environment variables should be stored in `.env.docker` file:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/plagiarism_dev

# Security
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin User (used for initial seeding)
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=AdminPass123!

# Storage
STORAGE_TYPE=local
S3_ENDPOINT_URL=http://minio:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET_NAME=plagiarism-uploads

# AI Detection
USE_EXTERNAL_AI_DETECTION=false
OPENAI_API_KEY=your-api-key
TOGETHER_API_KEY=your-api-key

# Celery & Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Development
ENVIRONMENT=development
```

### Database Seeding

The system automatically creates:
- Database tables on first startup
- Admin user account with credentials from environment variables
- Sample user accounts for testing

The seeding process happens automatically when the application starts up. You can also run the seeding script manually:

```bash
python -m app.core.database_seed
```
## Debugging

### Backend Debugging

1. Use logging for debugging:
```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

2. Run with debug flag:
```bash
uvicorn app.main:app --reload --debug
```

### Frontend Debugging

1. Use browser developer tools
2. Add console.log statements for debugging
3. Use React DevTools for component inspection

## Deployment Preparation

Before pushing to production:

1. Update version numbers
2. Run all tests
3. Update documentation if needed
4. Perform security audit
5. Test in staging environment

## Contributing Guidelines

1. Follow the existing code style
2. Write tests for new functionality
3. Update documentation for new features
4. Keep commits small and focused
5. Write clear commit messages
6. Address all CI/CD failures before merging

## Common Tasks

### Adding New Dependencies

Backend (using Poetry):
```bash
poetry add package-name
poetry export -o requirements.txt
```

Frontend (using npm):
```bash
npm install package-name
```

### Updating Documentation

1. Update README.md for major changes
2. Update technical documentation for architecture changes
3. Update API documentation for new endpoints

---

For questions or support, please open an issue in the repository.