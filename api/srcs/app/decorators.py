
import logging

from functools import wraps
from typing import Type

from fastapi import HTTPException, status

from tortoise.exceptions import DoesNotExist
from tortoise.models import Model


logger = logging.getLogger(__name__)

def handle_does_not_exists(model: Type[Model], status_code=status.HTTP_404_NOT_FOUND):
    """Transform a `DoesNotExist` error into a FastAPI HttpException"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except DoesNotExist as error:
                raise HTTPException(
                    status_code, f"{model.__name__} not found"
                ) from error

        return wrapper

    return decorator
