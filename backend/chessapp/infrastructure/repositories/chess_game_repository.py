import time
import logging
from opentelemetry import trace
from beanie import PydanticObjectId
from ...domain.game.chess_game import ChessGame
from ...infrastructure.factories.chess_game_factory import ChessGameFactory
from ...infrastructure.factories.game_document_factory import GameDocumentFactory
from ...infrastructure.factories.history_document_factory import GameHistoryDocumentFactory
from ...infrastructure.models import GameHistoryDocument
from ...infrastructure.models.game_document import GameDocument


class ChessGameRepository:
    logger = logging.getLogger("chessapp.repository")

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
        tracer = trace.get_tracer("chessapp.repository")
        
        with tracer.start_as_current_span("repository_find") as span:
            span.set_attribute("game_id", str(doc_id))
            
            with tracer.start_as_current_span("db_fetch_document"):
                start = time.time()
                document = await GameDocument.find_one(GameDocument.id == doc_id)
                # Fetch history manually to bypass slow fetch_links
                history_list = await GameHistoryDocument.find(GameHistoryDocument.game_id == doc_id).sort(+GameHistoryDocument.sequence_number).to_list()
                db_took = time.time() - start
                
            with tracer.start_as_current_span("factory_create_game"):
                factory_start = time.time()
                game = await ChessGameFactory.create(document, history_list)
                factory_took = time.time() - factory_start
            
            total = time.time() - start
            ChessGameRepository.logger.info(
                f"Repository.find({doc_id}): total={total:.4f}s (db={db_took:.4f}s, factory/restoration={factory_took:.4f}s)"
            )
            return game

    @staticmethod
    async def save(game: ChessGame):
        document = await GameDocument.find_one(GameDocument.id == game.game_id.value)
        history_documents = await GameHistoryDocumentFactory.create(game)

        # Optimization: Only insert NEW history documents
        current_len = len(document.history)
        new_len = len(history_documents)
        
        for i in range(current_len, new_len):
            history_document = history_documents[i]
            created_doc = await history_document.create()
            document.history.append(created_doc)

        try:
            start = time.time()
            document.game_name = game.information.name
            document.status = str(game.game_state.status)
            await document.save()
            save_took = time.time() - start
            ChessGameRepository.logger.info(f"Repository.save({game.game_id.value}): took {save_took:.4f}s")
        except Exception as e:
            print(f"Error updating game document: {e}")