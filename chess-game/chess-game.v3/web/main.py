from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.infrastructure.config.config import initiate_database
from web.api.main import api_router

@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    await initiate_database()

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

# to run - execute the command below
# fastapi dev main.py