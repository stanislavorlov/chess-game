from typing import List

from beanie import PydanticObjectId, Link
from beanie.odm.operators.find.logical import And
from beanie.odm.operators.update.general import Set
from bson import DBRef
from watchfiles import awatch

from chessapp.domain.game.chess_game import ChessGame
from chessapp.infrastructure.factories.chess_game_factory import ChessGameFactory
from chessapp.infrastructure.factories.game_document_factory import GameDocumentFactory
from chessapp.infrastructure.factories.history_document_factory import GameHistoryDocumentFactory
from chessapp.infrastructure.models import GameHistoryDocument
from chessapp.infrastructure.models.game_document import GameDocument


class ChessGameRepository:

    @staticmethod
    async def create(chess_game: ChessGame) -> ChessGame:

        # ToDo: Repository should invoke Factory to restore DB collection into Domain objects
        # ToDo: Repository should invoke Factory to save Domain into DB collection

        game_document = await GameDocumentFactory.create(chess_game)
        history_documents = await GameHistoryDocumentFactory.create(chess_game)

        for history_doc in history_documents:
            created_history = await history_doc.create()
            game_document.history.append(Link(created_history, GameHistoryDocument))

        created_game = await game_document.create()

        return await ChessGameRepository.find(created_game.id)

    @staticmethod
    async def find(doc_id: PydanticObjectId) -> ChessGame:
        #history = await GameHistoryDocument.find(GameHistoryDocument.game_id == doc_id, fetch_links=True).to_list()
        #print('fetched history')
        #print(history)

        document = await GameDocument.find_one(GameDocument.id == doc_id, fetch_links=True)

        return await ChessGameFactory.create(document)

        # created_documents = await GameCreatedDocument.find(
        #     And(
        #         GameCreatedDocument.game_id == document.id,
        #         GameCreatedDocument.action_type == 'game_created'
        #     )
        # ).to_list()
        #
        # game_started_documents = await GameStartedDocument.find(
        #     And(
        #         GameCreatedDocument.game_id == document.id,
        #         GameCreatedDocument.action_type == 'game_started'
        #     )
        # ).to_list()
        #
        # moved_documents = await PieceMovedDocument.find(
        #     And(
        #         PieceMovedDocument.game_id == document.id,
        #         PieceMovedDocument.action_type == 'piece_moved'
        #     )
        # ).to_list()
        #
        # captured_documents = await PieceCapturedDocument.find(
        #     And(
        #         PieceCapturedDocument.game_id == document.id,
        #         PieceCapturedDocument.action_type == 'piece_captured'
        #     )
        # ).to_list()
        #
        # # ToDo: separate translators for GameCreated and PieceMoved documents
        # return GameTranslator.document_to_domain(document,
        #                                          game_created_docs=created_documents,
        #                                          game_started_docs=game_started_documents,
        #                                          piece_moved_docs=moved_documents,
        #                                          piece_captured_docs=captured_documents)

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
        print('saving GameDocument')
        document = await GameDocument.find_one(GameDocument.id == game.game_id.value, fetch_links=True)
        history_documents = await GameHistoryDocumentFactory.create(game)

        print('History documents after factory:', len(history_documents))

        for history_document in history_documents:
            existing_doc = await GameHistoryDocument.get(history_document.id)
            if existing_doc is None:
                created_doc = await history_document.create()
                document.history.append(Link(created_doc, GameHistoryDocument))
            # else:
            #     document.history.append(Link(existing_doc, GameHistoryDocument))

        print('History document after DB save:', len(document.history))

        try:
            document.game_name = game.information.name
            await document.save()
        except Exception as e:
            print(f"Error updating game document: {e}")

        # history_document = []

        # history_document = GameHistoryTranslator.domain_to_document(
        #     game.game_id.value,
        #     document,
        #     game.history)

        # ToDo: retrieve existing history
        # ToDo: sequence number in DB with provided

        # ToDo: may be differentiate existing from the new ones via ID (or via sequence number)
        #histories = []
        #for created_history in history_document:
        #    histories.append(await created_history.create())