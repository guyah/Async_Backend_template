import logging
import asyncio
from tortoise import fields
from tortoise.models import Model
from typing import Literal


logger = logging.getLogger(__name__)


class Task(Model):
    id = fields.IntField(pk=True)
    celery_id = fields.CharField(max_length=64)
    status = fields.CharField(
        max_length=30,
        choices=['abort', 'failed', 'pending', 'running', 'succeeded'],
        default='pending'
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    ended_at = fields.DatetimeField(null=True)
    result = fields.JSONField(null=True)

    async def terminate(self, reason: str | None = None, **kwargs) -> None:
        from srcs.tasks.celery import worker

        logger.info(f"terminating task {self.celery_id} ({self.id})")
        worker.control.revoke(self.celery_id, terminate=True, signal='SIGTERM', **kwargs)
        self.status = "abort"
        if reason:
            self.result = {"reason": reason}
        await self.save()

    async def kill(self, reason: str | None = None, **kwargs) -> None:
        from srcs.tasks.celery import worker

        logger.info(f"killing task {self.celery_id} ({self.id})")
        worker.control.revoke(self.celery_id, terminate=True, signal='SIGKILL', **kwargs)
        self.status = "abort"
        if reason:
            self.result = {"reason": reason}
        await self.save()

    async def delete(self) -> None:
        if self.status in ('running', 'pending'):
            await self.terminate(reason="delete")
        await self.delete()


    async def terminate_or_kill(self, reason: str, timeout: int = 10):
        try:
            async with asyncio.Timeout(timeout):
                await self.terminate(reason="overwrited")
        except TimeoutError:
            await self.kill(reason="overwrited")


TaskStatus = Literal['abort', 'failed', 'pending', 'running', 'succeeded']
