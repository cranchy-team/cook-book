from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class RecipeBase(BaseModel):
    """Базовая схема рецепта."""

    title: str = Field(..., min_length=1, max_length=200, description="Название рецепта")
    ingredients: str = Field(..., description="Список ингредиентов")
    steps: str = Field(..., description="Шаги приготовления")
    cooking_time: int = Field(..., gt=0, description="Время приготовления в минутах")
    difficulty: str = Field(..., description="Сложность: easy, medium, hard")


class RecipeCreate(RecipeBase):
    """Схема для создания рецепта."""
    pass


class RecipeUpdate(BaseModel):
    """Схема для обновления рецепта."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    ingredients: Optional[str] = None
    steps: Optional[str] = None
    cooking_time: Optional[int] = Field(None, gt=0)
    difficulty: Optional[str] = None


class RecipeResponse(RecipeBase):
    """Схема ответа рецепта."""

    id: UUID
    user_id: UUID
    image_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
