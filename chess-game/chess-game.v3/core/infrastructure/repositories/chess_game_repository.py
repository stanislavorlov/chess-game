from beanie import PydanticObjectId

from core.domain.game.chess_game import ChessGame
from core.domain.game.game_format import GameFormat
from core.domain.game.game_history import ChessGameHistory
from core.domain.players.player_id import PlayerId
from core.domain.players.players import Players
from core.domain.value_objects.game_id import ChessGameId
from core.infrastructure.models.game_document import GameDocument

class ChessGameRepository:

    games_collection = GameDocument

    @staticmethod
    async def create(chess_game: ChessGame):
        new_game: GameDocument = GameDocument(name='', date='')
        game = await new_game.create()

        return ChessGame()

    # 67b0b58ed190d300f1fa60f9
    async def find(self, doc_id: PydanticObjectId) -> ChessGame:
        document = await self.games_collection.get(doc_id)

        game_id: ChessGameId = ChessGameId(document.game_id)
        players = Players(PlayerId(document.players.white_id), PlayerId(document.players.black_id))
        game_format = GameFormat.from_string(document.format.value, document.format.time_remaining)
        history = ChessGameHistory.empty()

        return ChessGame(game_id, game_format, history)

    async def find_by_id(self, game_id: ChessGameId) -> ChessGame:
        document = await self.games_collection.find_one(self.games_collection.game_id == game_id)

        players = Players(PlayerId(document.players.white_id), PlayerId(document.players.black_id))
        game_format = GameFormat.from_string(document.format.value, document.format.time_remaining)
        history = ChessGameHistory.empty()

        return ChessGame(game_id, game_format, history)

    async def save(self, game_id: PydanticObjectId, data: dict):
        des_body = {k: v for k, v in data.items() if v is not None}
        update_query = {"$set": {field: value for field, value in des_body.items()}}
        game = await self.games_collection.get(game_id)
        if game:
            await game.update(update_query)
            return game
        return False

        # bar = await Product.get("608da169eb9e17281f0ab2ff")
        # bar = await Product.find_one(Product.name == "Peanut Bar")
        # await bar.sync()
