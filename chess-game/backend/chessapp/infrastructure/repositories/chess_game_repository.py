from beanie import PydanticObjectId
from ...domain.game.chess_game import ChessGame
from ...infrastructure.factories.chess_game_factory import ChessGameFactory
from ...infrastructure.factories.game_document_factory import GameDocumentFactory
from ...infrastructure.factories.history_document_factory import GameHistoryDocumentFactory
from ...infrastructure.models import GameHistoryDocument
from ...infrastructure.models.game_document import GameDocument


class ChessGameRepository:

    @staticmethod
    async def create(chess_game: ChessGame) -> ChessGame:

        game_document = await GameDocumentFactory.create(chess_game)
        history_documents = await GameHistoryDocumentFactory.create(chess_game)

        for history_doc in history_documents:
            created_history = await history_doc.create()
            game_document.history.append(created_history)

        created_game = await game_document.create()

        return await ChessGameRepository.find(created_game.id)

    @staticmethod
    async def find(doc_id: PydanticObjectId) -> ChessGame:
        document = await GameDocument.find_one(GameDocument.id == doc_id, fetch_links=True)

        return await ChessGameFactory.create(document)

    @staticmethod
    async def save(game: ChessGame):
        document = await GameDocument.find_one(GameDocument.id == game.game_id.value, fetch_links=True)
        history_documents = await GameHistoryDocumentFactory.create(game)

        for history_document in history_documents:
            existing_doc = await GameHistoryDocument.get(history_document.id)
            if existing_doc is None:
                created_doc = await history_document.create()
                document.history.append(created_doc)

        try:
            document.game_name = game.information.name
            await document.save()
        except Exception as e:
            print(f"Error updating game document: {e}")