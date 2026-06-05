from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()

if "sqlite" in settings.DATABASE_URL:
    connect_args = {"check_same_thread": False}
else:
    connect_args = {"connect_timeout": 10}

engine = create_engine(
    settings.sqlalchemy_database_url,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency для получения сессии БД."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        