from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict
from beanie import init_beanie
from core.infrastructure import models


# https://fastapi.tiangolo.com/advanced/settings/#read-settings-from-env
class Settings(BaseSettings):
    MONGO_HOST: str = ''
    MONGO_DB: str = ''

    model_config = SettingsConfigDict(env_file=".env")

async def initiate_database():
    client = AsyncIOMotorClient(Settings().MONGO_HOST)
    await init_beanie(
        database=client.get_database(Settings().MONGO_DB),
        document_models=models.__all__
    )