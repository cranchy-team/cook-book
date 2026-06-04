import os
import logging
from typing import Optional
from fastapi import UploadFile
from ..config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

IMAGE_MAGIC_BYTES = {
    'image/jpeg': [b'\xff\xd8\xff'],
    'image/png': [b'\x89PNG\r\n\x1a\n'],
    'image/gif': [b'GIF87a', b'GIF89a'],
    'image/webp': [b'RIFF', b'WEBP']
}

MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_image_file(file: UploadFile) -> bool:
    """
    Валидация файла изображения.
    
    Args:
        file: Загружаемый файл
        
    Returns:
        True если файл валиден
        
    Raises:
        ValueError: Если файл невалиден
    """
    if not file.content_type or file.content_type not in IMAGE_MAGIC_BYTES:
        raise ValueError("Недопустимый тип файла. Разрешены только изображения (JPEG, PNG, GIF, WebP)")
    
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"Размер файла превышает {MAX_FILE_SIZE // (1024*1024)}MB")
    
    return True


def save_image(file: UploadFile, recipe_id: str) -> str:
    """
    Сохранение изображения рецепта.
    
    Args:
        file: Загружаемый файл
        recipe_id: ID рецепта для именования файла
        
    Returns:
        Относительный путь к сохраненному файлу
        
    Raises:
        ValueError: Если валидация не пройдена
        IOError: Если не удалось сохранить файл
    """
    validate_image_file(file)
    
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    
    file_extension = file.filename.split('.')[-1] if '.' in (file.filename or '') else 'jpg'
    filename = f"{recipe_id}.{file_extension}"
    filepath = os.path.join(upload_dir, filename)
    
    try:
        with open(filepath, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
        logger.info(f"Изображение сохранено: {filepath}")
        
        return f"uploads/{filename}"
    except Exception as e:
        logger.error(f"Ошибка сохранения файла: {e}")
        raise IOError(f"Не удалось сохранить файл: {e}")


def delete_image(image_path: str) -> bool:
    """
    Удаление изображения.
    
    Args:
        image_path: Относительный путь к файлу
        
    Returns:
        True если удалено
    """
    if not image_path:
        return False
    
    full_path = os.path.join(settings.UPLOAD_DIR, image_path.replace("uploads/", ""))
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
            logger.info(f"Изображение удалено: {full_path}")
            return True
    except Exception as e:
        logger.error(f"Ошибка удаления файла {full_path}: {e}")
    return False
