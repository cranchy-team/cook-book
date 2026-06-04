from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime
import base64
import logging

from ..models.recipe import Recipe
from ..schemas.recipe import RecipeCreate, RecipeUpdate

logger = logging.getLogger(__name__)


class RecipeService:
    """Сервис для работы с рецептами."""
    
    @staticmethod
    def create_recipe(db: Session, recipe_data: RecipeCreate, user_id: UUID) -> Recipe:
        """Создание нового рецепта."""
        db_recipe = Recipe(
            user_id=user_id,
            title=recipe_data.title,
            ingredients=recipe_data.ingredients,
            steps=recipe_data.steps,
            cooking_time=recipe_data.cooking_time,
            difficulty=recipe_data.difficulty,
            image_path=None
        )
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        logger.info(f"Рецепт создан: {db_recipe.id} пользователем {user_id}")
        return db_recipe
    
    @staticmethod
    def get_recipe(db: Session, recipe_id: UUID, user_id: UUID) -> Optional[Recipe]:
        """Получение рецепта по ID (только своего)."""
        return db.query(Recipe).filter(
            Recipe.id == recipe_id,
            Recipe.user_id == user_id
        ).first()
    
    @staticmethod
    def get_recipe_by_id(db: Session, recipe_id: UUID) -> Optional[Recipe]:
        """Получение рецепта по ID (для всех пользователей)."""
        return db.query(Recipe).filter(Recipe.id == recipe_id).first()
    
    @staticmethod
    def update_recipe(
        db: Session, 
        recipe_id: UUID, 
        user_id: UUID, 
        recipe_data: RecipeUpdate
    ) -> Optional[Recipe]:
        """Обновление рецепта."""
        db_recipe = RecipeService.get_recipe(db, recipe_id, user_id)
        if not db_recipe:
            return None
        
        update_data = recipe_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_recipe, field, value)
        
        db.commit()
        db.refresh(db_recipe)
        logger.info(f"Рецепт обновлен: {recipe_id}")
        return db_recipe
    
    @staticmethod
    def delete_recipe(db: Session, recipe_id: UUID, user_id: UUID) -> bool:
        """Удаление рецепта."""
        db_recipe = RecipeService.get_recipe(db, recipe_id, user_id)
        if not db_recipe:
            return False
        
        db.delete(db_recipe)
        db.commit()
        logger.info(f"Рецепт удален: {recipe_id}")
        return True
    
    @staticmethod
    def get_recipes(
        db: Session,
        user_id: Optional[UUID] = None,
        search: Optional[str] = None,
        difficulty: Optional[str] = None,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        limit: int = 20,
        cursor: Optional[str] = None
    ) -> Tuple[List[Recipe], Optional[str]]:
        """
        Получение списка рецептов с пагинацией на основе курсора.
        
        Args:
            db: Сессия БД
            user_id: ID пользователя (для фильтрации своих рецептов)
            search: Поиск по названию и ингредиентам
            difficulty: Фильтр по сложности
            created_after: Дата создания от
            created_before: Дата создания до
            limit: Максимальное количество рецептов
            cursor: Base64 кодированный курсор (created_at, id)
            
        Returns:
            Кортеж (список рецептов, следующий курсор)
        """
        query = db.query(Recipe)
        
        if user_id:
            query = query.filter(Recipe.user_id == user_id)
        
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Recipe.title.ilike(search_pattern),
                    Recipe.ingredients.ilike(search_pattern)
                )
            )
        
        if difficulty:
            query = query.filter(Recipe.difficulty == difficulty)
        
        if created_after:
            query = query.filter(Recipe.created_at >= created_after)
        if created_before:
            query = query.filter(Recipe.created_at <= created_before)
        
        if cursor:
            try:
                decoded = base64.b64decode(cursor).decode('utf-8')
                created_at_str, last_id = decoded.split('|')
                created_at = datetime.fromisoformat(created_at_str)
                
                query = query.filter(
                    or_(
                        and_(Recipe.created_at == created_at, Recipe.id < last_id),
                        Recipe.created_at < created_at
                    )
                )
            except Exception as e:
                logger.error(f"Ошибка парсинга курсора: {e}")
        
        query = query.order_by(Recipe.created_at.desc(), Recipe.id.desc())
        
        results = query.limit(limit + 1).all()
        
        has_next = len(results) > limit
        recipes = results[:limit] if has_next else results
        
        next_cursor = None
        if has_next and recipes:
            last_recipe = recipes[-1]
            cursor_data = f"{last_recipe.created_at.isoformat()}|{last_recipe.id}"
            next_cursor = base64.b64encode(cursor_data.encode('utf-8')).decode('utf-8')
        
        return recipes, next_cursor
    
    @staticmethod
    def get_user_recipe_count(db: Session, user_id: UUID) -> int:
        """Получение количества рецептов пользователя."""
        return db.query(Recipe).filter(Recipe.user_id == user_id).count()
