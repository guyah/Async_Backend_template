import asyncio

from tortoise import Tortoise
from srcs.config import cfg, TORTOISE_MODULES
from srcs.app.models import * 


asyncio.run(Tortoise.init(db_url=cfg.postgres_url, modules=TORTOISE_MODULES))