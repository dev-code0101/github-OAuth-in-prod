import httpx
from fastapi import HTTPException
from .models import FoodSearchResults, FoodItem, Serving


async def search_food(query: str, token: str):
    """Fetch food data from FatSecret API."""
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


async def process_food_data(food_data):
    """Process food data into Pydantic models."""
    if not food_data or "foods_search" not in food_data:
        raise HTTPException(status_code=404, detail="No food found.")

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

    return FoodSearchResults(food=foods)
