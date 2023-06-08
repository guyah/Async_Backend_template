import logging
from datetime import datetime

from celery import Celery, uuid
from celery import Task as CeleryTask
from celery._state import _task_stack
from tortoise import Tortoise, run_async

from srcs.config import TORTOISE_MODULES, cfg

from .models import Task
from .notif import emit
from .schemas import TaskSchema
import sentry_sdk

worker = Celery(__name__)
worker.conf.broker_url = cfg.celery.broker_url
worker.conf.result_backend = cfg.celery.result_backend
logger = logging.getLogger(__name__)


class DatabaseTask(CeleryTask):
    def __call__(self, *args, **kwargs):
        self.setup_sentry()
        return run_async(self.start(*args, **kwargs))

    async def connect_database(self) -> None:
        await Tortoise.init(db_url=cfg.postgres_url, modules=TORTOISE_MODULES)

    async def disconnect_database(self) -> None:
        await Tortoise.close_connections()

    def setup_sentry(self) -> None:
        if not cfg.sentry_dsn:
            return
        sentry_sdk.init(dsn=cfg.sentry_dsn, traces_sample_rate=1.0)


class ManagedTask(DatabaseTask):
    async def start(self, *args, **kwargs) -> None:
        _task_stack.push(self)
        await self.connect_database()
        task = await Task.get(celery_id=self.request.id)
        task.status = 'running'
        await task.save()
        await emit("TASK_CHANGED", await TaskSchema.from_tortoise_orm(task))

        try:
            task.result = await self.run(*args, **kwargs)
            task.status = 'succeeded'
            task.ended_at = datetime.utcnow()
        except Exception as error:
            task.result = {"error": str(error)}
            task.status = 'failed'
            task.ended_at = datetime.utcnow()
            sentry_sdk.capture_exception(error)
            raise error
        finally:
            self.pop_request()
            _task_stack.push(self)
            await task.save()
            await emit("TASK_CHANGED", await TaskSchema.from_tortoise_orm(task))
            await self.disconnect_database()

    async def delay(self, *args, **kwargs) -> Task:
        task = await Task.create(celery_id=uuid())
        await emit("TASK_CHANGED", await TaskSchema.from_tortoise_orm(task))
        self.apply_async(args=args, kwargs=kwargs, task_id=task.celery_id)
        return task


class OrphanTask(DatabaseTask):
    """Asyncio capable task but without a Task in db to follow it's status
    """
    async def start(self, *args, **kwargs) -> None:
        _task_stack.push(self)
        await self.connect_database()
        try:
            await self.run(*args, **kwargs)
        finally:
            self.pop_request()
            _task_stack.push(self)
            await self.disconnect_database()

    def delay(self, *args, **kwargs):
        return self.apply_async(args=args, kwargs=kwargs)
