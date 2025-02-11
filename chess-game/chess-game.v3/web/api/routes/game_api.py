from typing import Mapping, Any

from fastapi import APIRouter, Request
from pymongo.synchronous.database import Database

router = APIRouter(prefix="/game")

@router.get("/{game_id}")
async def start(game_id, request: Request):
    # print('API DB')
    # print(request.app.mongodb)
    #
    # for coll in request.app.mongodb.list_collection_names():
    #     print(coll)
    #
    # return request.app.mongodb.movies.find_one()

    movies = []
    for doc in request.app.mongodb["movies"].find().limit(10):\
        movies.append(str(doc["title"]))
    return movies
