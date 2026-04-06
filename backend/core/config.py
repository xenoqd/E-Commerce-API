from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    DATABASE_URL: str
    DATABASE_URL_ALEMBIC: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    PENDING_STATUS_UPDATE_EVERY: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
