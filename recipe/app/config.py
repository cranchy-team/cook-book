from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Конфигурация приложения."""

    DATABASE_URL: str
    JWT_SECRET: str
    RECIPE_SERVICE_PORT: str = "8080"
    UPLOAD_DIR: str = "/app/static/uploads"

    @property
    def sqlalchemy_database_url(self) -> str:
        """Возвращает URL для SQLAlchemy (заменяет postgres:// на postgresql://)."""
        return self.DATABASE_URL.replace("postgres://", "postgresql://")

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Получение конфигурации с кэшированием."""
    return Settings()
