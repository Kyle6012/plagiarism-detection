from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from app.models.user import User
from app.models.batch import Batch
from app.models.document import Document
from app.core.db import get_user_db, get_db
from app.core.auth import auth_backend
from sqlalchemy.orm import Session
from sqlalchemy import select, func
import uuid

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_db,
    [auth_backend],
)

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)

@router.get("/users/me/dashboard")
async def get_user_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.current_user())
):
    num_batches = await db.execute(
        select(func.count(Batch.id)).where(Batch.user_id == user.id)
    ).scalar_one()

    num_documents = await db.execute(
        select(func.count(Document.id))
        .join(Batch, Document.batch_id == Batch.id)
        .where(Batch.user_id == user.id)
    ).scalar_one()

    return {
        "status": "ok",
        "data": {
            "num_batches": num_batches,
            "num_documents": num_documents,
        },
    }
