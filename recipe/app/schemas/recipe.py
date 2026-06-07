from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
DIFFICULTY_TRANSLATIONS = {
    "easy": "Легкий",
    "medium": "Средний",
    "hard": "Сложный"
}

MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 1440

MIN_TITLE_LENGTH = 1
MAX_TITLE_LENGTH = 200

MIN_INGREDIENTS_LENGTH = 1
MAX_INGREDIENTS_LENGTH = 5000
MIN_STEPS_LENGTH = 1
MAX_STEPS_LENGTH = 10000


class RecipeBase(BaseModel):

    title: str = Field(
        ...,
        min_length=MIN_TITLE_LENGTH,
        max_length=MAX_TITLE_LENGTH,
        description="Название рецепта (1-200 символов)"
    )
    ingredients: str = Field(
        ...,
        min_length=MIN_INGREDIENTS_LENGTH,
        max_length=MAX_INGREDIENTS_LENGTH,
        description="Список ингредиентов (1-5000 символов)"
    )
    steps: str = Field(
        ...,
        min_length=MIN_STEPS_LENGTH,
        max_length=MAX_STEPS_LENGTH,
        description="Шаги приготовления (1-10000 символов)"
    )
    cooking_time: int = Field(
        ...,
        ge=MIN_COOKING_TIME,
        le=MAX_COOKING_TIME,
        description=f"Время приготовления в минутах ({MIN_COOKING_TIME}-{MAX_COOKING_TIME})"
    )
    difficulty: str = Field(
        ...,
        description=f"Сложность: {', '.join(DIFFICULTY_LEVELS)}"
    )

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        v_lower = v.lower().strip()
        if v_lower not in DIFFICULTY_LEVELS:
            raise ValueError(
                f"Недопустимое значение сложности. "
                f"Разрешенные значения: {', '.join(DIFFICULTY_LEVELS)}. "
                f"Вы ввели: '{v}'"
            )
        return v_lower

    @field_validator("cooking_time")
    @classmethod
    def validate_cooking_time(cls, v: int) -> int:
        if v < MIN_COOKING_TIME:
            raise ValueError(
                f"Время приготовления не может быть меньше {MIN_COOKING_TIME} минуты. "
                f"Вы ввели: {v}"
            )
        if v > MAX_COOKING_TIME:
            raise ValueError(
                f"Время приготовления не может превышать {MAX_COOKING_TIME} минут (24 часа). "
                f"Вы ввели: {v}"
            )
        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Название рецепта не может быть пустым")
        return v

    @field_validator("ingredients")
    @classmethod
    def validate_ingredients(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Список ингредиентов не может быть пустым")
        return v

    @field_validator("steps")
    @classmethod
    def validate_steps(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Шаги приготовления не могут быть пустыми")
        return v


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):

    title: Optional[str] = Field(
        None,
        min_length=MIN_TITLE_LENGTH,
        max_length=MAX_TITLE_LENGTH,
        description="Название рецепта (1-200 символов)"
    )
    ingredients: Optional[str] = Field(
        None,
        min_length=MIN_INGREDIENTS_LENGTH,
        max_length=MAX_INGREDIENTS_LENGTH,
        description="Список ингредиентов (1-5000 символов)"
    )
    steps: Optional[str] = Field(
        None,
        min_length=MIN_STEPS_LENGTH,
        max_length=MAX_STEPS_LENGTH,
        description="Шаги приготовления (1-10000 символов)"
    )
    cooking_time: Optional[int] = Field(
        None,
        ge=MIN_COOKING_TIME,
        le=MAX_COOKING_TIME,
        description=f"Время приготовления в минутах ({MIN_COOKING_TIME}-{MAX_COOKING_TIME})"
    )
    difficulty: Optional[str] = Field(
        None,
        description=f"Сложность: {', '.join(DIFFICULTY_LEVELS)}"
    )

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v_lower = v.lower().strip()
        if v_lower not in DIFFICULTY_LEVELS:
            raise ValueError(
                f"Недопустимое значение сложности. "
                f"Разрешенные значения: {', '.join(DIFFICULTY_LEVELS)}. "
                f"Вы ввели: '{v}'"
            )
        return v_lower

    @field_validator("cooking_time")
    @classmethod
    def validate_cooking_time(cls, v: Optional[int]) -> Optional[int]:
        if v is None:
            return v
        if v < MIN_COOKING_TIME:
            raise ValueError(
                f"Время приготовления не может быть меньше {MIN_COOKING_TIME} минуты. "
                f"Вы ввели: {v}"
            )
        if v > MAX_COOKING_TIME:
            raise ValueError(
                f"Время приготовления не может превышать {MAX_COOKING_TIME} минут (24 часа). "
                f"Вы ввели: {v}"
            )
        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Проверяет, что title не пустой и trimmed."""
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Название рецепта не может быть пустым")
        return v

    @field_validator("ingredients")
    @classmethod
    def validate_ingredients(cls, v: Optional[str]) -> Optional[str]:
        """Проверяет, что ingredients не пустой."""
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Список ингредиентов не может быть пустым")
        return v

    @field_validator("steps")
    @classmethod
    def validate_steps(cls, v: Optional[str]) -> Optional[str]:
        """Проверяет, что steps не пустой."""
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Шаги приготовления не могут быть пустыми")
        return v


class RecipeResponse(RecipeBase):

    id: UUID
    user_id: UUID
    image_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DifficultyLevels(BaseModel):
    
    levels: List[str] = DIFFICULTY_LEVELS
    translations: dict = DIFFICULTY_TRANSLATIONS
