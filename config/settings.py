import os

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    MONGO_DB_NAME: str = os.environ.get('MONGO_DB_NAME')
    OPENAI_API_KEY: str = os.environ.get('OPENAI_API_KEY')


class LocalConfig(Settings):
    HOST: str = os.getenv('MONGO_HOST', 'localhost')
    MONGO_PORT: str = os.getenv("MONGO_PORT", "27017")
    MONGO_DB_URL: str = f'mongodb://{HOST}:{MONGO_PORT}'
    DEBUG: bool = True


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna una instancia cacheada de la configuración
    """
    settings = LocalConfig()
    return settings
