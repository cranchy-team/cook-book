from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPCookie
from datetime import datetime
from .config import get_settings

settings = get_settings()

security = HTTPCookie(auto_error=False)


def verify_jwt_token(token: str) -> dict:
    """
    Верификация JWT токена.
    
    Args:
        token: JWT токен
        
    Returns:
        Payload токена с user_id
        
    Raises:
        HTTPException: Если токен невалиден
    """
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=["HS256"]
        )
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный токен: отсутствует user_id"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось аутентифицировать пользователя"
        )


async def get_current_user(token: str = Depends(security)) -> dict:
    """
    Dependency для получения текущего пользователя из JWT токена.
    
    Args:
        token: JWT токен из cookie
        
    Returns:
        Payload токена
        
    Raises:
        HTTPException: Если токен отсутствует или невалиден
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен отсутствует"
        )
    return verify_jwt_token(token)


async def get_current_user_optional(token: str = Depends(security)) -> dict | None:
    """
    Опциональная аутентификация - возвращает None если токен не предоставлен.
    
    Args:
        token: JWT токен из cookie
        
    Returns:
        Payload токена или None
    """
    if not token:
        return None
    try:
        return verify_jwt_token(token)
    except HTTPException:
        return None
