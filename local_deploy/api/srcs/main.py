import logging
import sys
from contextlib import asynccontextmanager
from typing import Any

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_socketio import SocketManager
from tortoise import Tortoise

from tortoise.contrib.fastapi import register_tortoise
from srcs.app.models import Placeholder

from srcs.config import TORTOISE_MODULES, cfg

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    if cfg.sentry_dsn:
        logger.info("enabling sentry")
        sentry_sdk.init(
            dsn=cfg.sentry_dsn,
            traces_sample_rate=1.0,
            integrations=[
                StarletteIntegration(transaction_style="endpoint"),
                FastApiIntegration(transaction_style="endpoint"),
            ],
        )

    register_tortoise(
        app,
        db_url=cfg.postgres_url,
        modules=TORTOISE_MODULES,
        generate_schemas=True,
        add_exception_handlers=True
    )
    # seems to be necessary to be able to use "execute_query" from this context
    logger.debug("connecting database")
    await Tortoise.init(db_url=cfg.postgres_url, modules=TORTOISE_MODULES)
    await Tortoise.get_connection("default").execute_query("CREATE EXTENSION IF NOT EXISTS vector;")
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()
    logger.debug('disconnected from database')


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = SocketManager(
    app=app,
    mount_location='/ws',
    cors_allowed_origins=[]
)

@app.sio.on('connect')
async def handle_connect(sid, *args, **kwargs):
    logger.debug(f'{sid} connected')


@app.sio.on('join')
async def handle_join(sid, *args, **kwargs):
    logging.debug(f'{sid} joined')
    await sio.emit('join', {'success': True}, sid)


@app.sio.on('loopback')
async def handle_loopback(sid, message: str):
    await sio.emit('broadcast', message, sid)


@app.post('/broadcast', status_code=204)
async def broadcast(data: Any = Body(...)) -> None:
    await sio.emit('broadcast', data)


@app.post("/notif/emit", status_code=204)
async def send_notification(event: str = Body(...), payload: Any = Body(...)) -> None:
    await sio.emit(event, payload)

@app.post("/sample")
async def create_sample():
    temp = await Placeholder.create(name="test")
    await temp.save()
    return {f"Created {temp}"}

@app.get('/health')
def health():
    return {'healthy': True}
