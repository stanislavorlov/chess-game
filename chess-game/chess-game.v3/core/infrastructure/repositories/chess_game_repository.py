from beanie import PydanticObjectId
from beanie.odm.operators.update.general import Set
from core.domain.game.chess_game import ChessGame
from core.infrastructure.models.game_document import GameDocument
from core.infrastructure.models.game_history_document import GameCreatedDocument, PieceMovedDocument
from core.infrastructure.translators.game_history_translator import GameHistoryTranslator
from core.infrastructure.translators.game_translator import GameTranslator


class ChessGameRepository:

    @staticmethod
    async def create(chess_game: ChessGame) -> ChessGame:
        game_document = GameTranslator.domain_to_document(chess_game)
        history_document = GameHistoryTranslator.domain_to_document(chess_game.game_id.value, game_document, chess_game.history)

        created_game = await game_document.create()
        histories = []
        for created_history in history_document:
            histories.append(await created_history.create())

        return GameTranslator.document_to_domain(created_game, histories, [])

    @staticmethod
    async def find(doc_id: PydanticObjectId) -> ChessGame:
        document = await GameDocument.get(doc_id, fetch_links=True)

        created_documents = await GameCreatedDocument.find(
            GameCreatedDocument.game_id == document.id and
            GameCreatedDocument.action_type == 'game_created').to_list()

        moved_documents = await PieceMovedDocument.find(
            PieceMovedDocument.game_id == document.id and
            PieceMovedDocument.action_type == 'piece_moved').to_list()

        # ToDo: separate translators for GameCreated and PieceMoved documents
        return GameTranslator.document_to_domain(document, created_documents, moved_documents)

    # async def find_by_id(self, game_id: ChessGameId) -> ChessGame:
    #     document = await GameDocument.find_one(GameDocument.game_id == game_id.value, fetch_links=True)
    #     histories = await GameHistoryDocument.find(GameHistoryDocument.game_id == document.game_id).to_list()
    #
    #     for history in histories:
    #         print(history)
    #
    #     return GameTranslator.document_to_domain(document, histories)

    # async def save(self, game_id: PydanticObjectId, data: dict):
    #     des_body = {k: v for k, v in data.items() if v is not None}
    #     update_query = {"$set": {field: value for field, value in des_body.items()}}
    #     game = await self.games_collection.get(game_id)
    #     if game:
    #         await game.update(update_query)
    #         return game
    #     return False

    @staticmethod
    async def save(game: ChessGame):
        document = await GameDocument.get(game.game_id.value)

        await document.update(Set(
            {
                GameDocument.state.status: str(game.game_state.get_status()),
                GameDocument.game_name: game.information.name,
            }
        ))

        history_document = GameHistoryTranslator.domain_to_document(
            game.game_id.value,
            document,
            game.history)

        # ToDo: retrieve existing history
        # ToDo: sequence number in DB with provided

        # ToDo: may be differentiate existing from the new ones via ID (or via sequence number)
        histories = []
        for created_history in history_document:
            histories.append(await created_history.create())