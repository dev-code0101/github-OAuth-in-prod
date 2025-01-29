from .oauth import get_oauth_token

from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.models import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Security(oauth2_scheme)) -> TokenData:
    if not token:
        raise HTTPException(
            status_code=401, detail="Invalid authentication token"
        )

    return TokenData(access_token=token, token_type="bearer")


async def get_db() -> AsyncSession:
    async with get_session() as session:
        yield session


async def get_current_token(code: str) -> TokenData:
    """OAuth2 Dependency for retrieving current token."""
    token_data = await get_oauth_token(code)
    return TokenData(**token_data)
