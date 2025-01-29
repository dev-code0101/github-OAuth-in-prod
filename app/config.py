import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET")
    REDIRECT_URI: str = os.getenv(
        "REDIRECT_URI", "http://localhost:8000/callback"
    )
    AUTHORIZATION_BASE_URL: str = "https://github.com/login/oauth/authorize"
    TOKEN_URL: str = "https://github.com/login/oauth/access_token"
    API_BASE_URL: str = "https://api.github.com/user"
    DATABASE_URL: str = os.getenv('DATABASE_URL')


settings = Settings()
