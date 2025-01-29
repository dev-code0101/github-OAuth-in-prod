import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_search_food(client: AsyncClient):
    response = await client.get("/search_food/apple")

    assert response.status_code in [200, 404]  # Could return food or not found
    assert "food" in response.json() or "message" in response.json()
