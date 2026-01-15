# Deployment Guide: Plagiarism & AI Detection System

This guide provides comprehensive instructions for deploying the plagiarism and AI detection system in various environments.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Docker Deployment](#docker-deployment)
3. [Environment Variables](#environment-variables)
4. [Initial Setup and Seeding](#initial-setup-and-seeding)
5. [Production Deployment](#production-deployment)
6. [Scaling Considerations](#scaling-considerations)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Prerequisites

- Docker Engine (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- At least 8GB RAM (recommended 16GB for heavy loads)
- 10GB free disk space
- Ports 80 and 8000 available

## Docker Deployment

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/your-username/plagiarism-detection.git
cd plagiarism-detection
```

2. Create environment file:
```bash
cp backend/.env.docker.example backend/.env.docker
```

3. Edit the environment variables as needed (see Environment Variables section below)

4. Start the services:
```bash
docker-compose up --build -d
```

5. Access the application:
   - Frontend: http://localhost
   - API Docs: http://localhost:8000/docs

### Services Architecture

The system consists of the following services:

- **Frontend**: React/Vite application served by Nginx
- **API**: FastAPI backend with security and authentication
- **Database**: PostgreSQL with pgvector extension for similarity search
- **Redis**: Message broker for Celery task queue
- **MinIO**: S3-compatible storage for document uploads
- **Celery Workers**: Background processing for analysis tasks
- **Celery Beat**: Scheduled tasks management

## Environment Variables

All environment variables are configured in `backend/.env.docker`. Here's a breakdown of each:

### Database Configuration
```env
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/plagiarism_db
```
- Connection string for PostgreSQL database
- Uses asyncpg driver for async operations

### Security Configuration
```env
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
- `SECRET_KEY`: Cryptographic key for JWT tokens (must be strong and unique)
- `ALGORITHM`: JWT signing algorithm (HS256 recommended)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Admin User Configuration
```env
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=AdminPass123!
```
- `ADMIN_EMAIL`: Email for the initial admin user account
- `ADMIN_PASSWORD`: Password for the initial admin user account

### Storage Configuration
```env
STORAGE_TYPE=s3  # or 'local'
S3_ENDPOINT_URL=http://minio:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET_NAME=plagiarism-uploads
```
- `STORAGE_TYPE`: Set to 's3' for MinIO or 'local' for filesystem storage
- `S3_*`: MinIO credentials and endpoint (when using S3 storage)

### AI Detection Configuration
```env
USE_EXTERNAL_AI_DETECTION=false
OPENAI_API_KEY=your-openai-api-key
TOGETHER_API_KEY=your-together-api-key
```
- `USE_EXTERNAL_AI_DETECTION`: Enable/disable external AI providers
- `OPENAI_API_KEY`: OpenAI API key for GPT-based detection
- `TOGETHER_API_KEY`: Together AI API key for alternative models

### Celery & Redis Configuration
```env
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```
- Redis connection settings for Celery task queue
- Same URL used for both broker and result backend

### Application Environment
```env
ENVIRONMENT=production  # or 'development'
```
- Controls CORS settings and debug modes

## Initial Setup and Seeding

The system automatically creates the database tables and seeds initial data on first startup:

1. **Automatic Database Creation**: Tables are created automatically on first run
2. **Admin Account Creation**: An admin user is created with credentials from environment variables
3. **Sample Users**: Default users are created for testing purposes

### Admin Credentials

On first startup, the system creates an admin account using these environment variables:
- `ADMIN_EMAIL`: Email for the admin account (defaults to admin@example.com)
- `ADMIN_PASSWORD`: Password for the admin account (defaults to AdminPass123!)

### Sample User Accounts

The following sample accounts are created automatically:
- user1@example.com (password: UserPass123!)
- user2@example.com (password: UserPass123!)
- moderator@example.com (password: ModPass123!)

## Production Deployment

### Security Hardening

1. **Secret Keys**: Generate a strong secret key for production:
```bash
python -c 'import secrets; print(secrets.token_urlsafe(32))'
```

2. **Admin Credentials**: Change default admin credentials before production use

3. **HTTPS**: Use a reverse proxy (nginx, Apache) with SSL termination in front of the application

3. **Database Security**: 
   - Use strong passwords for database access
   - Enable SSL for database connections in production
   - Regular backups

4. **Network Security**:
   - Limit exposed ports to only necessary ones
   - Use internal networks for service-to-service communication
   - Implement rate limiting

### Performance Tuning

1. **Celery Workers**: Adjust worker count based on CPU cores:
```yaml
# In docker-compose.yml
command: celery -A app.core.celery.app worker -l info -c 4  # 4 workers
```

2. **Database Pooling**: Optimize connection pooling in production

3. **Caching**: Implement Redis caching for frequently accessed data

### Docker Compose Production Optimizations

```yaml
version: '3.8'

services:
  db:
    image: ankane/pgvector:v0.5.1
    restart: unless-stopped
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=secure_password
      - POSTGRES_DB=plagiarism_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    # Add health check
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d plagiarism_db"]
      interval: 30s
      timeout: 10s
      retries: 3

  api:
    build:
      context: .
      dockerfile: backend/Dockerfile
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    # Add resource limits
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
```

## Scaling Considerations

### Horizontal Scaling

1. **API Layer**: Scale multiple API instances behind a load balancer
2. **Celery Workers**: Add more worker instances for increased processing capacity
3. **Database**: Consider read replicas for database scaling
4. **Storage**: MinIO supports distributed mode for high availability

### Vertical Scaling

1. **CPU**: AI processing is CPU-intensive; allocate more cores for better performance
2. **Memory**: Large documents and models require substantial RAM
3. **Storage**: Plan for document storage growth

### Load Distribution

- Use a load balancer (nginx, HAProxy) for multiple API instances
- Configure sticky sessions if needed for file uploads
- Distribute Celery workers across multiple machines if needed

## Monitoring and Maintenance

### Health Checks

- API: `GET /health` - Returns basic health status
- AI Service: `GET /api/v1/ai-detection/health` - AI service status

### Logging

- Application logs are available in Docker containers
- Monitor Celery worker logs for background job status
- Database query performance logs

### Backup Strategy

1. **Database**: Regular PostgreSQL dumps
2. **Documents**: Backup MinIO/S3 storage regularly
3. **Configuration**: Version control for Docker compose and environment files

### Updates

1. Pull latest code: `git pull origin main`
2. Rebuild containers: `docker-compose build --no-cache`
3. Restart services: `docker-compose up -d --force-recreate`

## Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 80 and 8000 are available
2. **Insufficient Resources**: Increase allocated memory/CPU if experiencing timeouts
3. **Connection Issues**: Verify all service dependencies are running

### Logs Access

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs api
docker-compose logs celery-worker
docker-compose logs db
```

### Performance Issues

- Monitor CPU and memory usage
- Check database query performance
- Review Celery task processing times
- Optimize AI model loading and processing

---

For support or questions, please open an issue in the repository.