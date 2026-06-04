from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Cookie
from datetime import datetime
from ..config import get_settings

settings = get_settings()


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


async def get_current_user(access_token: str = Cookie(None)) -> dict:
    """
    Dependency для получения текущего пользователя из JWT токена.
    
    Args:
        access_token: JWT токен из cookie
        
    Returns:
        Payload токена
        
    Raises:
        HTTPException: Если токен отсутствует или невалиден
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен отсутствует"
        )
    return verify_jwt_token(access_token)


async def get_current_user_optional(access_token: str = Cookie(None)) -> dict | None:
    """
    Опциональная аутентификация - возвращает None если токен не предоставлен.
    
    Args:
        access_token: JWT токен из cookie
        
    Returns:
        Payload токена или None
    """
    if not access_token:
        return None
    try:
        return verify_jwt_token(access_token)
    except HTTPException:
        return None
