import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, OAuthToken
from app.config import settings
from oauthlib.oauth2 import WebApplicationClient

client = WebApplicationClient(settings.CLIENT_ID)
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_API_URL = "https://api.github.com/user"


async def get_oauth_token(db: AsyncSession, code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_URL,
            data={
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        token_data = response.json()

    if "access_token" not in token_data:
        return None

    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            USER_API_URL,
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        user_data = user_response.json()

    # Check if user exists
    existing_user = await db.execute(
        User.__table__.select().where(User.github_id == str(user_data["id"]))
    )
    user = existing_user.scalar_one_or_none()

    if not user:
        user = User(
            github_id=str(user_data["id"]),
            username=user_data["login"],
            email=user_data.get("email"),
            avatar_url=user_data["avatar_url"],
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # Store OAuth Token
    token = OAuthToken(
        access_token=token_data["access_token"],
        token_type=token_data["token_type"],
        scope=token_data.get("scope", ""),
        user_id=user.id,
    )
    db.add(token)
    await db.commit()

    return user
