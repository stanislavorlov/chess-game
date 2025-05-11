from beanie import PydanticObjectId
from beanie.odm.operators.find.logical import And
from beanie.odm.operators.update.general import Set
from chessapp.domain.game.chess_game import ChessGame
from chessapp.infrastructure.models.game_document import GameDocument
from chessapp.infrastructure.models.game_history_document import GameCreatedDocument, PieceMovedDocument, \
    GameStartedDocument, PieceCapturedDocument
from chessapp.infrastructure.translators.game_history_translator import GameHistoryTranslator
from chessapp.infrastructure.translators.game_translator import GameTranslator


class ChessGameRepository:

    @staticmethod
    async def create(chess_game: ChessGame) -> ChessGame:
        # ToDo: translators into Factory or AutoMappers
        game_document = GameTranslator.domain_to_document(chess_game)
        history_document = GameHistoryTranslator.domain_to_document(chess_game.game_id.value, game_document, chess_game.history)

        created_game = await game_document.create()
        histories = []
        for created_history in history_document:
             histories.append(await created_history.create())
             return GameTranslator.document_to_domain(created_game, histories, [], [], [])

        return await ChessGameRepository.find(created_game.id)

    @staticmethod
    async def find(doc_id: PydanticObjectId) -> ChessGame:
        document = await GameDocument.get(doc_id, fetch_links=True)

        created_documents = await GameCreatedDocument.find(
            And(
                GameCreatedDocument.game_id == document.id,
                GameCreatedDocument.action_type == 'game_created'
            )
        ).to_list()

        game_started_documents = await GameStartedDocument.find(
            And(
                GameCreatedDocument.game_id == document.id,
                GameCreatedDocument.action_type == 'game_started'
            )
        ).to_list()

        moved_documents = await PieceMovedDocument.find(
            And(
                PieceMovedDocument.game_id == document.id,
                PieceMovedDocument.action_type == 'piece_moved'
            )
        ).to_list()

        captured_documents = await PieceCapturedDocument.find(
            And(
                PieceCapturedDocument.game_id == document.id,
                PieceCapturedDocument.action_type == 'piece_captured'
            )
        ).to_list()

        # ToDo: separate translators for GameCreated and PieceMoved documents
        return GameTranslator.document_to_domain(document,
                                                 game_created_docs=created_documents,
                                                 game_started_docs=game_started_documents,
                                                 piece_moved_docs=moved_documents,
                                                 piece_captured_docs=captured_documents)

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
                # GameDocument.state.captured:
                # GameDocument.format.time_remaining
                # GameDocument.format.additional_time
                GameDocument.state.turn: game.game_state.turn.value(),
                #GameDocument.state.status: str(game.game_state.get_status()),
                GameDocument.game_name: game.information.name,
                # GameDocument.result
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