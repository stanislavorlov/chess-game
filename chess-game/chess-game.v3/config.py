from pydantic_settings import BaseSettings, SettingsConfigDict

# https://fastapi.tiangolo.com/advanced/settings/#read-settings-from-env
class Settings(BaseSettings):
    MONGO_HOST: str = ''
    MONGO_DB: str = ''

    model_config = SettingsConfigDict(env_file=".env")