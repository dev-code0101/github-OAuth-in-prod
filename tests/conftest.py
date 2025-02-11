import pytest_asyncio as pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.db import get_db, engine
from app.models import Base


# Override the database session to use an in-memory test database
@pytest.fixture(scope="function")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = get_db()
    yield session
    await session.close()


# Override the database dependency for tests
@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(base_url="http://testserver") as ac:
        yield ac
