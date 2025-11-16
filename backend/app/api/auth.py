from fastapi_users import FastAPIUsers
from app.models.user import User
from app.core.db import get_user_db
from app.core.auth import auth_backend
from fastapi import APIRouter
import uuid
from app.schemas import UserRead, UserCreate

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_db,
    [auth_backend],
)

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
