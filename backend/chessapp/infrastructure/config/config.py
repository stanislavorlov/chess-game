from pydantic_settings import BaseSettings, SettingsConfigDict


import os

# https://fastapi.tiangolo.com/advanced/settings/#read-settings-from-env
class Settings(BaseSettings):
    MONGO_HOST: str = ''
    MONGO_DB: str = ''
    REDIS_URL: str = 'redis://localhost:6379'
    KAFKA_BOOTSTRAP_SERVERS: str = 'localhost:9092'

    # Dynamically resolve absolute path to backend/chessapp/.env
    model_config = SettingsConfigDict(
        env_file=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
    )