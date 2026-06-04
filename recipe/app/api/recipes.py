from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
import logging

from ..database import get_db
from ..auth.jwt import get_current_user
from ..services.recipe_service import RecipeService
from ..schemas.recipe import RecipeCreate, RecipeUpdate, RecipeResponse
from ..utils.file_handler import save_image, delete_image

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recipes", tags=["Рецепты"])


@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe_data: RecipeCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    user_id = user["user_id"]
    recipe = RecipeService.create_recipe(db, recipe_data, user_id)
    return recipe


@router.get("/", response_model=List[RecipeResponse])
async def get_recipes(
    search: Optional[str] = Query(None, description="Поиск по названию и ингредиентам"),
    difficulty: Optional[str] = Query(None, description="Фильтр по сложности"),
    created_after: Optional[datetime] = Query(None, description="Дата создания от"),
    created_before: Optional[datetime] = Query(None, description="Дата создания до"),
    limit: int = Query(20, ge=1, le=100, description="Максимальное количество рецептов"),
    cursor: Optional[str] = Query(None, description="Курсор для пагинации"),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    recipes, next_cursor = RecipeService.get_recipes(
        db=db,
        user_id=user["user_id"],
        search=search,
        difficulty=difficulty,
        created_after=created_after,
        created_before=created_before,
        limit=limit,
        cursor=cursor
    )
    
    from fastapi import Response
    response = Response()
    if next_cursor:
        response.headers["X-Next-Cursor"] = next_cursor
    
    return recipes


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(
    recipe_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    recipe = RecipeService.get_recipe(db, recipe_id, user["user_id"])
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рецепт не найден"
        )
    return recipe


@router.put("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: UUID,
    recipe_data: RecipeUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    recipe = RecipeService.update_recipe(db, recipe_id, user["user_id"], recipe_data)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рецепт не найден"
        )
    return recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    success = RecipeService.delete_recipe(db, recipe_id, user["user_id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рецепт не найден"
        )
    return None


@router.post("/{recipe_id}/upload-image", response_model=RecipeResponse)
async def upload_recipe_image(
    recipe_id: UUID,
    image: UploadFile = File(..., description="Изображение рецепта"),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    recipe = RecipeService.get_recipe(db, recipe_id, user["user_id"])
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рецепт не найден"
        )
    
    if recipe.image_path:
        delete_image(recipe.image_path)
    
    image_path = save_image(image, str(recipe_id))
    recipe.image_path = image_path
    db.commit()
    db.refresh(recipe)
    
    return recipe
