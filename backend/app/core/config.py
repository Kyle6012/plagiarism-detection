from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # Optional: External AI Detection APIs
    OPENAI_API_KEY: Optional[str] = ""  # For GPT-based AI detection
    ZEROGPT_API_KEY: Optional[str] = ""  # For ZeroGPT API
    COPYLEAKS_API_KEY: Optional[str]  = ""  # For CopyLeaks plagiarism API
    
    # Optional: Use external APIs instead of local models
    USE_EXTERNAL_AI_DETECTION: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
