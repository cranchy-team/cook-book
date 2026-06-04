from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import logging

from ..models.favorite import Favorite
from ..models.recipe import Recipe

logger = logging.getLogger(__name__)


class FavoriteService:
    """Сервис для работы с избранным."""

    @staticmethod
    def add_to_favorites(db: Session, user_id: UUID, recipe_id: UUID) -> Favorite:
        """
        Добавление рецепта в избранное (идемпотентная операция).

        Args:
            db: Сессия БД
            user_id: ID пользователя
            recipe_id: ID рецепта

        Returns:
            Созданная/существующая запись избранного
        """
        existing = db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.recipe_id == recipe_id
        ).first()

        if existing:
            logger.info(f"Рецепт {recipe_id} уже в избранном у пользователя {user_id}")
            return existing

        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise ValueError(f"Рецепт {recipe_id} не найден")

        favorite = Favorite(
            user_id=user_id,
            recipe_id=recipe_id
        )
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        logger.info(f"Рецепт {recipe_id} добавлен в избранное пользователем {user_id}")
        return favorite

    @staticmethod
    def remove_from_favorites(db: Session, user_id: UUID, recipe_id: UUID) -> bool:
        """
        Удаление рецепта из избранного.

        Args:
            db: Сессия БД
            user_id: ID пользователя
            recipe_id: ID рецепта

        Returns:
            True если удалено, False если не было в избранном
        """
        favorite = db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.recipe_id == recipe_id
        ).first()

        if not favorite:
            return False

        db.delete(favorite)
        db.commit()
        logger.info(f"Рецепт {recipe_id} удален из избранного пользователем {user_id}")
        return True

    @staticmethod
    def get_favorites(db: Session, user_id: UUID, limit: int = 50) -> List[Recipe]:
        """
        Получение списка избранных рецептов пользователя.

        Args:
            db: Сессия БД
            user_id: ID пользователя
            limit: Максимальное количество

        Returns:
            Список рецептов
        """
        favorites = db.query(Favorite).filter(Favorite.user_id == user_id).limit(limit).all()

        recipe_ids = [f.recipe_id for f in favorites]
        recipes = db.query(Recipe).filter(Recipe.id.in_(recipe_ids)).all()

        return recipes

    @staticmethod
    def is_favorite(db: Session, user_id: UUID, recipe_id: UUID) -> bool:
        """Проверка, есть ли рецепт в избранном."""
        favorite = db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.recipe_id == recipe_id
        ).first()
        return favorite is not None
