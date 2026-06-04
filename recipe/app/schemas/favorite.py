from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class FavoriteCreate(BaseModel):
    """Схема для добавления в избранное."""
    
    user_id: UUID
    recipe_id: UUID


class FavoriteResponse(BaseModel):
    """Схема ответа избранного."""
    
    user_id: UUID
    recipe_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
