from beanie import PydanticObjectId
from core.domain.game.chess_game import ChessGame
from core.domain.value_objects.game_id import ChessGameId
from core.infrastructure.models import GameHistoryDocument
from core.infrastructure.models.game_document import GameDocument
from core.infrastructure.translators.game_history_translator import GameHistoryTranslator
from core.infrastructure.translators.game_translator import GameTranslator


class ChessGameRepository:

    games_collection = GameDocument
    games_history_collection = GameHistoryDocument

    @staticmethod
    async def create(chess_game: ChessGame) -> ChessGame:
        game_document = GameTranslator.domain_to_document(chess_game)
        created_game = await game_document.create()

        history_document = GameHistoryTranslator.domain_to_document(chess_game.game_id.value, chess_game.history)
        for created_history in history_document:
            await created_history.create()

        return await GameTranslator.document_to_domain(created_game)

    # 67b0b58ed190d300f1fa60f9
    async def find(self, doc_id: PydanticObjectId) -> ChessGame:
        document = await self.games_collection.get(doc_id, fetch_links=True)
        # document = await GameDocument.find(GameDocument.id == doc_id, fetch_links=True).to_list()

        return await GameTranslator.document_to_domain(document)

    async def find_by_id(self, game_id: ChessGameId) -> ChessGame:
        document = await self.games_collection.find_one(GameDocument.game_id == game_id.value, fetch_links=True)

        return await GameTranslator.document_to_domain(document)

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
