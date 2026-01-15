import loguru
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.admin import router as admin_router
from app.core.db import async_engine
from app.models.base import Base


app = FastAPI()

# CORS Middleware - Restrict origins in production
allowed_origins = ["http://localhost:5173", "http://localhost:80"]
if os.getenv("ENVIRONMENT") == "development":
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
from app.api import routes, auth, users
from app.api.v1 import routes as v1_routes

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(admin_router, prefix="/api", tags=["admin"])
app.include_router(v1_routes.router, prefix="/api/v1", tags=["analysis"])
app.include_router(routes.router, prefix="/api/v1", tags=["legacy"]) # Keep legacy routes for now or deprecate


@app.on_event("startup")
async def startup_event():
    loguru.logger.info("Starting up...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed the database with initial data
    try:
        from app.core.database_seed import seed_database
        await seed_database()
    except Exception as e:
        loguru.logger.error(f"Database seeding failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    loguru.logger.info("Shutting down...")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Plagiarism Detection API", "status": "running"}
