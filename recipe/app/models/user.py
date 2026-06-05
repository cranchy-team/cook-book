from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base
import uuid


class User(Base):
    """Заглушка пользователя для foreign key (основная модель в auth-сервисе)."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), nullable=False)
