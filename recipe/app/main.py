from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from .config import get_settings
from .database import engine, Base
from .api import recipes_router, favorites_router

settings = get_settings()

from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cook Book Recipe Service",
    description="API для управления рецептами в приложении Cook Book",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Создаем директорию для загрузок, если она не существует
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Монтируем статические файлы для доступа к изображениям
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:80", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Регистрация роутеров
app.include_router(recipes_router, prefix="/api/v1")
app.include_router(favorites_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "recipe-service"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Cook Book Recipe Service", "version": "1.0.0"}
