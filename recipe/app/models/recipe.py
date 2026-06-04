from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..database import Base
import uuid


class Recipe(Base):
    """Модель рецепта."""

    __tablename__ = "recipes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    ingredients = Column(Text, nullable=False)
    steps = Column(Text, nullable=False)
    cooking_time = Column(Integer, nullable=False)
    difficulty = Column(String(20), nullable=False)
    image_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
