import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./library.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
