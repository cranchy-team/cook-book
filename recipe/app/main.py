from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import os
import logging
from .config import get_settings
from .database import engine, Base
from .api import recipes_router, favorites_router
from .models import Recipe, Favorite, User  # noqa: F401 pylint: disable=unused-import

logger = logging.getLogger(__name__)

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cook Book Recipe Service",
    description="API для управления рецептами в приложении Cook Book",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:80", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(f"Validation error: {errors}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Ошибка валидации данных",
            "details": errors
        }
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(f"Pydantic validation error: {errors}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Ошибка валидации данных",
            "details": errors
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {type(exc).__name__} - {str(exc)}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Внутренняя ошибка сервера",
            "detail": "Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже."
        }
    )


app.include_router(recipes_router, prefix="/api/v1")
app.include_router(favorites_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "recipe-service"}


@app.get("/")
async def root():
    return {"message": "Cook Book Recipe Service", "version": "1.0.0"}
