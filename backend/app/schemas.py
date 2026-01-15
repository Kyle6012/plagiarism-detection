import uuid
from fastapi_users import schemas
from typing import Optional
from pydantic import BaseModel

class UserRead(schemas.BaseUser[uuid.UUID]):
    role: str = "user"

class UserCreate(schemas.BaseUserCreate):
    role: Optional[str] = "user"

class UserUpdate(schemas.BaseUserUpdate):
    role: Optional[str] = None
