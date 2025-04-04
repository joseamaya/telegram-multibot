import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pyngrok import ngrok

import routers
from dependencies import bot_manager
from utils import setup_ngrok, setup_telegram

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    tokens = [os.environ.get('TELEGRAM_TOKEN')]
    for token in tokens:
        bot_manager.add_bot(token)

    await bot_manager.initialize_all()
    public_url = setup_ngrok()

    for token in tokens:
        await setup_telegram(token, public_url)

    yield

    await bot_manager.shutdown_all()
    if public_url:
        ngrok.disconnect(public_url)

app = FastAPI(lifespan=lifespan)

app.include_router(routers.router)