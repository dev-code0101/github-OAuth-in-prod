from fastapi import FastAPI
from app.routes import auth, food
from app.db import engine
from app.models import Base

# Initialize FastAPI
app = FastAPI(title="FastAPI OAuth App", version="1.0.0")

# Include Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(food.router, prefix="/food", tags=["Food Search"])


# Initialize database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI OAuth App"}
