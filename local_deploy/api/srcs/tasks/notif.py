from pydantic import BaseModel
from typing import Any
import logging
from srcs.main import sio

logger = logging.getLogger(__name__)


async def emit(event: str, payload: Any) -> bool:
    """Emits a notification from the worker.
    contact the notification endpoint on the main api
    """
    if isinstance(payload, BaseModel):
        payload = payload.json()
    logger.info(f"Sending event {event} with payload {payload}")
    await sio.emit(event, payload)
