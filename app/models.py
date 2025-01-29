from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
import datetime


class Serving(BaseModel):
    serving_description: str
    calories: float
    carbohydrate: float
    protein: float
    fat: float
    saturated_fat: float
    sodium: float
    potassium: float
    fiber: float
    sugar: float
    serving_url: str


class FoodItem(BaseModel):
    food_id: str
    food_name: str
    brand_name: str
    food_url: str
    food_type: str
    servings: list[Serving]


class FoodSearchResults(BaseModel):
    food: list[FoodItem]


class TokenData(BaseModel):
    access_token: str
    token_type: str


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    oauth_tokens = relationship("OAuthToken", back_populates="user")


class OAuthToken(Base):
    __tablename__ = "oauth_tokens"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, unique=True)
    token_type = Column(String)
    scope = Column(String)
    expires_at = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="oauth_tokens")
