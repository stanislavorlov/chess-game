from beanie import PydanticObjectId

from core.infrastructure.models.game_document import GameDocument

class ChessGameRepository:

    games_collection = GameDocument

    @staticmethod
    async def create(new_game: GameDocument):
        game = await new_game.create()
        return game

    # 67b0b58ed190d300f1fa60f9
    async def find(self, game_id: PydanticObjectId) -> GameDocument:
        game = await self.games_collection.get(game_id)
        return game

    async def save(self, game_id: PydanticObjectId, data: dict):
        des_body = {k: v for k, v in data.items() if v is not None}
        update_query = {"$set": {field: value for field, value in des_body.items()}}
        student = await self.games_collection.get(game_id)
        if student:
            await student.update(update_query)
            return student
        return False
