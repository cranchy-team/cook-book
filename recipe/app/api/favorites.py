from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import logging

from ..database import get_db
from ..auth.jwt import get_current_user
from ..services.favorite_service import FavoriteService
from ..models.recipe import Recipe
from ..schemas.favorite import FavoriteResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/favorites", tags=["Избранное"])


@router.post("/{recipe_id}", response_model=FavoriteResponse)
async def add_to_favorites(
    recipe_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Добавление рецепта в избранное.
    
    Идемпотентная операция - если рецепт уже в избранном, вернет существующую запись.
    """
    try:
        favorite = FavoriteService.add_to_favorites(db, user["user_id"], recipe_id)
        return favorite
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_favorites(
    recipe_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Удаление рецепта из избранного.
    """
    success = FavoriteService.remove_from_favorites(db, user["user_id"], recipe_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рецепт не найден в избранном"
        )
    return None


@router.get("/", response_model=List[Recipe])
async def get_favorites(
    limit: int = 50,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Получение списка избранных рецептов пользователя.
    """
    favorites = FavoriteService.get_favorites(db, user["user_id"], limit)
    return favorites


@router.get("/{recipe_id}/status", response_model=FavoriteResponse)
async def check_favorite_status(
    recipe_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Проверка, есть ли рецепт в избранном.
    """
    if not FavoriteService.is_favorite(db, user["user_id"], recipe_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рецепт не найден в избранном"
        )
    
    favorite = db.query(Favorite).filter(
        Favorite.user_id == user["user_id"],
        Favorite.recipe_id == recipe_id
    ).first()
    
    return favorite
