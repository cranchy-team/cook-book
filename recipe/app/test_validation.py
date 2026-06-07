import pytest
from pydantic import ValidationError
from datetime import datetime
from uuid import uuid4

from .schemas.recipe import (
    RecipeCreate,
    RecipeUpdate,
    DIFFICULTY_LEVELS,
    MIN_COOKING_TIME,
    MAX_COOKING_TIME
)


class TestRecipeCreateValidation:

    def test_valid_recipe(self):
        recipe = RecipeCreate(
            title="Борщ",
            ingredients="Свёкла, капуста, картофель",
            steps="1. Варим мясо\n2. Режем овощи\n3. Варим борщ",
            cooking_time=120,
            difficulty="medium"
        )
        assert recipe.title == "Борщ"
        assert recipe.difficulty == "medium"
        assert recipe.cooking_time == 120

    def test_difficulty_case_insensitive(self):
        for diff in ["EASY", "Medium", "HARD", "easy", "medium", "hard"]:
            recipe = RecipeCreate(
                title="Тест",
                ingredients="Ингредиенты",
                steps="Шаги",
                cooking_time=30,
                difficulty=diff
            )
            assert recipe.difficulty in DIFFICULTY_LEVELS

    def test_difficulty_invalid(self):
        with pytest.raises(ValidationError) as exc_info:
            RecipeCreate(
                title="Тест",
                ingredients="Ингредиенты",
                steps="Шаги",
                cooking_time=30,
                difficulty="super_hard"
            )
        assert "Недопустимое значение сложности" in str(exc_info.value)

    def test_cooking_time_min(self):
        recipe = RecipeCreate(
            title="Тест",
            ingredients="Ингредиенты",
            steps="Шаги",
            cooking_time=MIN_COOKING_TIME,
            difficulty="easy"
        )
        assert recipe.cooking_time == 1

    def test_cooking_time_max(self):
        recipe = RecipeCreate(
            title="Тест",
            ingredients="Ингредиенты",
            steps="Шаги",
            cooking_time=MAX_COOKING_TIME,
            difficulty="hard"
        )
        assert recipe.cooking_time == 1440

    def test_cooking_time_too_small(self):
        with pytest.raises(ValidationError) as exc_info:
            RecipeCreate(
                title="Тест",
                ingredients="Ингредиенты",
                steps="Шаги",
                cooking_time=0,
                difficulty="easy"
            )
        assert "greater_than_equal" in str(exc_info.value) or "не может быть меньше" in str(exc_info.value)

    def test_cooking_time_too_large(self):
        with pytest.raises(ValidationError) as exc_info:
            RecipeCreate(
                title="Тест",
                ingredients="Ингредиенты",
                steps="Шаги",
                cooking_time=2000,
                difficulty="easy"
            )
        assert "less_than_equal" in str(exc_info.value) or "не может превышать" in str(exc_info.value)

    def test_title_max_length(self):
        long_title = "A" * 200
        recipe = RecipeCreate(
            title=long_title,
            ingredients="Ингредиенты",
            steps="Шаги",
            cooking_time=30,
            difficulty="easy"
        )
        assert recipe.title == long_title

    def test_title_too_long(self):
        with pytest.raises(ValidationError) as exc_info:
            RecipeCreate(
                title="A" * 201,
                ingredients="Ингредиенты",
                steps="Шаги",
                cooking_time=30,
                difficulty="easy"
            )
        assert "string_too_long" in str(exc_info.value) or "200" in str(exc_info.value)

    def test_title_whitespace_trimmed(self):
        recipe = RecipeCreate(
            title="  Борщ  ",
            ingredients="Ингредиенты",
            steps="Шаги",
            cooking_time=30,
            difficulty="easy"
        )
        assert recipe.title == "Борщ"

    def test_title_empty(self):
        with pytest.raises(ValidationError) as exc_info:
            RecipeCreate(
                title="",
                ingredients="Ингредиенты",
                steps="Шаги",
                cooking_time=30,
                difficulty="easy"
            )
        assert "string_too_short" in str(exc_info.value) or "пустым" in str(exc_info.value).lower()

    def test_ingredients_whitespace_trimmed(self):
        recipe = RecipeCreate(
            title="Тест",
            ingredients="  Свёкла, капуста  ",
            steps="Шаги",
            cooking_time=30,
            difficulty="easy"
        )
        assert recipe.ingredients == "Свёкла, капуста"

    def test_steps_whitespace_trimmed(self):
        recipe = RecipeCreate(
            title="Тест",
            ingredients="Ингредиенты",
            steps="  1. Шаг 1\n  2. Шаг 2  ",
            cooking_time=30,
            difficulty="easy"
        )
        assert recipe.steps == "1. Шаг 1\n  2. Шаг 2"


class TestRecipeUpdateValidation:

    def test_partial_update(self):
        update = RecipeUpdate(title="Новый борщ")
        assert update.title == "Новый борщ"
        assert update.ingredients is None
        assert update.steps is None

    def test_full_update(self):
        update = RecipeUpdate(
            title="Новый борщ",
            ingredients="Новые ингредиенты",
            steps="Новые шаги",
            cooking_time=60,
            difficulty="hard"
        )
        assert update.title == "Новый борщ"
        assert update.cooking_time == 60
        assert update.difficulty == "hard"

    def test_update_invalid_difficulty(self):
        with pytest.raises(ValidationError) as exc_info:
            RecipeUpdate(difficulty="impossible")
        assert "Недопустимое значение сложности" in str(exc_info.value)

    def test_update_cooking_time_negative(self):
        with pytest.raises(ValidationError) as exc_info:
            RecipeUpdate(cooking_time=-10)
        assert "greater_than_equal" in str(exc_info.value) or "не может быть меньше" in str(exc_info.value)

    def test_update_empty_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            RecipeUpdate(title="")
        assert "string_too_short" in str(exc_info.value) or "пустым" in str(exc_info.value).lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
