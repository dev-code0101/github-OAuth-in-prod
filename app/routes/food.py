from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import (
    FoodItem,
    FoodSearchResults,
    TokenData,
    Serving,
)  # Import models from models.py
from app.dependencies import get_db, get_current_user
import httpx

router = APIRouter()


# Function to search food using OAuth2 token
async def search_food(query: str, token: str):
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://platform.fatsecret.com/rest/foods/search/v3",
            params={"search_expression": query, "max_results": 5},
            headers=headers,
        )
        if response.status_code == 200:
            return response.json()
        return None


# Search food endpoint (Requires authentication)
@router.get("/search_food/{query}", response_model=FoodSearchResults)
async def search_food_endpoint(
    query: str,
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user),
):
    food_data = await search_food(query, user.access_token)

    if food_data and "foods_search" in food_data:
        foods = [
            FoodItem(
                food_id=item["food_id"],
                food_name=item["food_name"],
                brand_name=item["brand_name"],
                food_url=item["food_url"],
                food_type=item["food_type"],
                servings=[
                    Serving(
                        serving_description=serving["serving_description"],
                        calories=float(serving["calories"]),
                        carbohydrate=float(serving["carbohydrate"]),
                        protein=float(serving["protein"]),
                        fat=float(serving["fat"]),
                        saturated_fat=float(serving["saturated_fat"]),
                        sodium=float(serving["sodium"]),
                        potassium=float(serving["potassium"]),
                        fiber=float(serving["fiber"]),
                        sugar=float(serving["sugar"]),
                        serving_url=serving["serving_url"],
                    )
                    for serving in item["servings"]["serving"]
                ],
            )
            for item in food_data["foods_search"]["results"]["food"]
        ]

        return {"food": foods}

    raise HTTPException(status_code=404, detail="No food found.")
