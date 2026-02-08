from pydantic_settings import BaseSettings, SettingsConfigDict


# https://fastapi.tiangolo.com/advanced/settings/#read-settings-from-env
class Settings(BaseSettings):
    MONGO_HOST: str = ''
    MONGO_DB: str = ''
    REDIS_URL: str = 'redis://localhost:6379'
    KAFKA_BOOTSTRAP_SERVERS: str = 'localhost:9092'

    model_config = SettingsConfigDict(env_file=".env")