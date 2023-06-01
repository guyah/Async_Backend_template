import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.sio.on('connect')
async def handle_connect(sid, *args, **kwargs):
    logger.debug(f'{sid} connected')

@app.sio.on('join')
async def handle_join(sid, *args, **kwargs):
    logging.debug(f'{sid} joined')

@app.get('/health')
def health():
    return {'healthy': True}
