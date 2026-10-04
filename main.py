import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.store.mongodb import MongoDBStore
from pyngrok import ngrok

import routers
from ai.store import get_index_config
from config.settings import get_settings
from dependencies import bot_manager
from utils import setup_ngrok, setup_telegram

settings = get_settings()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    tokens = [os.environ.get('TELEGRAM_TOKEN')]
    public_url = None

    with MongoDBSaver.from_conn_string(
        settings.MONGO_DB_URL,
        db_name=settings.MONGO_DB_NAME,
    ) as checkpointer:
        with MongoDBStore.from_conn_string(
            settings.MONGO_DB_URL,
            db_name=settings.MONGO_DB_NAME,
            collection_name="memories",
            index_config=get_index_config(),
        ) as store:
            for token in tokens:
                bot_manager.add_bot(token, store=store, checkpointer=checkpointer)

            await bot_manager.initialize_all()
            public_url = setup_ngrok()

            for token in tokens:
                await setup_telegram(token, public_url)

            try:
                yield
            finally:
                await bot_manager.shutdown_all()
                if public_url:
                    ngrok.disconnect(public_url)

app = FastAPI(lifespan=lifespan)

app.include_router(routers.router)
