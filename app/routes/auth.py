from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.oauth import get_oauth_token

from app.config import settings

router = APIRouter()


@router.get("/login")
async def login():
    authorization_url = f"https://github.com/login/oauth/authorize?client_id={settings.CLIENT_ID}"
    return {"authorization_url": authorization_url}


@router.get("/callback")
async def callback(code: str, db: AsyncSession = Depends(get_db)):
    user = await get_oauth_token(db, code)
    if user:
        return {"user": {"id": user.id, "username": user.username}}
    return {"error": "Authentication failed"}
