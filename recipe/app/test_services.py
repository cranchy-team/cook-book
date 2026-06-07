import pytest
from unittest.mock import Mock
from datetime import datetime
from uuid import uuid4
import base64

from .services.recipe_service import RecipeService
from .services.favorite_service import FavoriteService
from .models.recipe import Recipe
from .schemas.recipe import RecipeCreate, RecipeUpdate


@pytest.fixture
def mock_db():
    db = Mock()
    db.query = Mock()
    db.add = Mock()
    db.delete = Mock()
    db.commit = Mock()
    db.refresh = Mock()
    return db


@pytest.fixture
def mock_user_id():
    return uuid4()


@pytest.fixture
def mock_recipe_id():
    return uuid4()


@pytest.fixture
def mock_recipe_data():
    return RecipeCreate(
        title="Тестовый борщ",
        ingredients="Свёкла, капуста, картофель",
        steps="1. Варим мясо\n2. Режем овощи\n3. Варим борщ",
        cooking_time=120,
        difficulty="medium"
    )


@pytest.fixture
def mock_recipe(mock_user_id, mock_recipe_data):
    return Recipe(
        id=uuid4(),
        user_id=mock_user_id,
        title=mock_recipe_data.title,
        ingredients=mock_recipe_data.ingredients,
        steps=mock_recipe_data.steps,
        cooking_time=mock_recipe_data.cooking_time,
        difficulty=mock_recipe_data.difficulty,
        image_path=None,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


class TestCreateRecipe:

    def test_create_recipe_success(self, mock_db, mock_user_id, mock_recipe_data):
        mock_recipe = Mock()
        mock_recipe.id = uuid4()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_recipe

        result = RecipeService.create_recipe(mock_db, mock_recipe_data, mock_user_id)

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert result is not None
        assert hasattr(result, 'id')

    def test_create_recipe_all_fields(self, mock_db, mock_user_id, mock_recipe_data):
        mock_recipe = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_recipe

        RecipeService.create_recipe(mock_db, mock_recipe_data, mock_user_id)

        call_args = mock_db.add.call_args[0][0]
        assert call_args.user_id == mock_user_id
        assert call_args.title == mock_recipe_data.title
        assert call_args.ingredients == mock_recipe_data.ingredients
        assert call_args.steps == mock_recipe_data.steps
        assert call_args.cooking_time == mock_recipe_data.cooking_time
        assert call_args.difficulty == mock_recipe_data.difficulty
        assert call_args.image_path is None


class TestGetRecipe:

    def test_get_recipe_exists(self, mock_db, mock_user_id, mock_recipe_id, mock_recipe):
        mock_db.query.return_value.filter.return_value.first.return_value = mock_recipe

        result = RecipeService.get_recipe(mock_db, mock_recipe_id, mock_user_id)

        assert result == mock_recipe
        mock_db.query.assert_called_once()

    def test_get_recipe_not_found(self, mock_db, mock_user_id, mock_recipe_id):
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = RecipeService.get_recipe(mock_db, mock_recipe_id, mock_user_id)

        assert result is None

    def test_get_recipe_only_own(self, mock_db, mock_user_id, mock_recipe_id):
        mock_db.query.return_value.filter.return_value.first.return_value = None

        RecipeService.get_recipe(mock_db, mock_recipe_id, mock_user_id)

        filter_call = mock_db.query.return_value.filter
        filter_call.assert_called_once()


class TestUpdateRecipe:

    def test_update_recipe_success(self, mock_db, mock_user_id, mock_recipe_id, mock_recipe):
        mock_db.query.return_value.filter.return_value.first.return_value = mock_recipe
        update_data = RecipeUpdate(title="Новый борщ")

        result = RecipeService.update_recipe(mock_db, mock_recipe_id, mock_user_id, update_data)

        assert result == mock_recipe
        assert mock_recipe.title == "Новый борщ"
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    def test_update_recipe_not_found(self, mock_db, mock_user_id, mock_recipe_id):
        mock_db.query.return_value.filter.return_value.first.return_value = None
        update_data = RecipeUpdate(title="Новый борщ")

        result = RecipeService.update_recipe(mock_db, mock_recipe_id, mock_user_id, update_data)

        assert result is None
        mock_db.commit.assert_not_called()

    def test_update_recipe_partial(self, mock_db, mock_user_id, mock_recipe_id, mock_recipe):
        mock_db.query.return_value.filter.return_value.first.return_value = mock_recipe
        update_data = RecipeUpdate(cooking_time=60)

        RecipeService.update_recipe(mock_db, mock_recipe_id, mock_user_id, update_data)

        assert mock_recipe.cooking_time == 60
        assert mock_recipe.title == "Тестовый борщ"


class TestDeleteRecipe:

    def test_delete_recipe_success(self, mock_db, mock_user_id, mock_recipe_id, mock_recipe):
        mock_db.query.return_value.filter.return_value.first.return_value = mock_recipe

        result = RecipeService.delete_recipe(mock_db, mock_recipe_id, mock_user_id)

        assert result is True
        mock_db.delete.assert_called_once_with(mock_recipe)
        mock_db.commit.assert_called_once()

    def test_delete_recipe_not_found(self, mock_db, mock_user_id, mock_recipe_id):
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = RecipeService.delete_recipe(mock_db, mock_recipe_id, mock_user_id)

        assert result is False
        mock_db.delete.assert_not_called()
        mock_db.commit.assert_not_called()


class TestGetRecipes:

    def test_get_recipes_no_filters(self, mock_db, mock_user_id, mock_recipe):
        mock_db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = [mock_recipe]

        recipes, next_cursor = RecipeService.get_recipes(mock_db, user_id=mock_user_id, limit=20)

        assert len(recipes) == 1
        assert next_cursor is None

    def test_get_recipes_with_search(self, mock_db, mock_user_id, mock_recipe):
        mock_db.query.return_value.filter.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = [mock_recipe]

        recipes, _ = RecipeService.get_recipes(mock_db, user_id=mock_user_id, search="борщ")

        assert len(recipes) == 1

    def test_get_recipes_with_difficulty_filter(self, mock_db, mock_user_id, mock_recipe):
        mock_db.query.return_value.filter.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = [mock_recipe]

        recipes, _ = RecipeService.get_recipes(mock_db, user_id=mock_user_id, difficulty="medium")

        assert len(recipes) == 1

    def test_get_recipes_with_cursor(self, mock_db, mock_user_id, mock_recipe):
        mock_recipe.created_at = datetime.now()
        mock_db.query.return_value.filter.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = [mock_recipe]

        cursor_data = f"{mock_recipe.created_at.isoformat()}|{mock_recipe.id}"
        cursor = base64.b64encode(cursor_data.encode('utf-8')).decode('utf-8')

        recipes, next_cursor = RecipeService.get_recipes(mock_db, user_id=mock_user_id, cursor=cursor, limit=20)

        assert len(recipes) == 1

    def test_get_recipes_has_next_page(self, mock_db, mock_user_id):
        mock_recipes = [Mock() for _ in range(21)]
        for i, r in enumerate(mock_recipes):
            r.id = uuid4()
            r.created_at = datetime.now()

        mock_db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = mock_recipes

        recipes, next_cursor = RecipeService.get_recipes(mock_db, user_id=mock_user_id, limit=20)

        assert len(recipes) == 20
        assert next_cursor is not None

    def test_get_recipes_no_next_page(self, mock_db, mock_user_id, mock_recipe):
        mock_db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = [mock_recipe]

        recipes, next_cursor = RecipeService.get_recipes(mock_db, user_id=mock_user_id, limit=20)

        assert len(recipes) == 1
        assert next_cursor is None


class TestGetUserRecipeCount:

    def test_count_recipes(self, mock_db, mock_user_id):
        mock_db.query.return_value.filter.return_value.count.return_value = 5

        result = RecipeService.get_user_recipe_count(mock_db, mock_user_id)

        assert result == 5


class TestAddToFavorites:

    def test_add_to_favorites_new(self, mock_db, mock_user_id, mock_recipe_id):
        mock_recipe = Mock()
        mock_db.query.return_value.filter.return_value.first.side_effect = [None, mock_recipe]
        mock_db.query.return_value.filter.return_value.add.return_value = None

        result = FavoriteService.add_to_favorites(mock_db, mock_user_id, mock_recipe_id)

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        assert result is not None

    def test_add_to_favorites_already_exists(self, mock_db, mock_user_id, mock_recipe_id):
        mock_existing = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_existing

        result = FavoriteService.add_to_favorites(mock_db, mock_user_id, mock_recipe_id)

        assert result == mock_existing
        mock_db.add.assert_not_called()
        mock_db.commit.assert_not_called()

    def test_add_to_favorites_recipe_not_found(self, mock_db, mock_user_id, mock_recipe_id):
        mock_db.query.return_value.filter.return_value.first.side_effect = [None, None]

        with pytest.raises(ValueError, match="Рецепт .* не найден"):
            FavoriteService.add_to_favorites(mock_db, mock_user_id, mock_recipe_id)


class TestRemoveFromFavorites:

    def test_remove_from_favorites_exists(self, mock_db, mock_user_id, mock_recipe_id):
        mock_favorite = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_favorite

        result = FavoriteService.remove_from_favorites(mock_db, mock_user_id, mock_recipe_id)

        assert result is True
        mock_db.delete.assert_called_once_with(mock_favorite)
        mock_db.commit.assert_called_once()

    def test_remove_from_favorites_not_exists(self, mock_db, mock_user_id, mock_recipe_id):

        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = FavoriteService.remove_from_favorites(mock_db, mock_user_id, mock_recipe_id)

        assert result is False
        mock_db.delete.assert_not_called()
        mock_db.commit.assert_not_called()


class TestGetFavorites:

    def test_get_favorites_empty(self, mock_db, mock_user_id):
        mock_db.query.return_value.filter.return_value.limit.return_value.all.return_value = []
        mock_db.query.return_value.filter.return_value.all.return_value = []

        result = FavoriteService.get_favorites(mock_db, mock_user_id)

        assert result == []

    def test_get_favorites_with_recipes(self, mock_db, mock_user_id, mock_recipe):
        mock_favorite = Mock()
        mock_favorite.recipe_id = mock_recipe.id
        mock_db.query.return_value.filter.return_value.limit.return_value.all.return_value = [mock_favorite]
        mock_db.query.return_value.filter.return_value.all.return_value = [mock_recipe]

        result = FavoriteService.get_favorites(mock_db, mock_user_id)

        assert len(result) == 1
        assert result[0] == mock_recipe

    def test_get_favorites_limit(self, mock_db, mock_user_id):
        mock_db.query.return_value.filter.return_value.limit.return_value.all.return_value = []

        FavoriteService.get_favorites(mock_db, mock_user_id, limit=10)

        mock_db.query.return_value.filter.return_value.limit.assert_called_with(10)


class TestIsFavorite:

    def test_is_favorite_true(self, mock_db, mock_user_id, mock_recipe_id):
        mock_db.query.return_value.filter.return_value.first.return_value = Mock()

        result = FavoriteService.is_favorite(mock_db, mock_user_id, mock_recipe_id)

        assert result is True

    def test_is_favorite_false(self, mock_db, mock_user_id, mock_recipe_id):
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = FavoriteService.is_favorite(mock_db, mock_user_id, mock_recipe_id)

        assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
