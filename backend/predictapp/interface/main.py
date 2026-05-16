import asyncio
import logging
import grpc
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from predictapp.ai.bitboards import Bitboards, Side
from predictapp.ai.keras_model import ChessZeroModel
from predictapp.ai.mcts import MonteCarloTreeSearch
from predictapp.interface.rpc import chessai_pb2_grpc, chessai_pb2

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("predictapp")

def index_to_square(index: int) -> str:
    file = index % 8
    rank = index // 8
    return chr(ord('a') + file) + str(rank + 1)

class AiService(chessai_pb2_grpc.AiServiceServicer):
    def __init__(self):
        logger.info("Initializing ChessZero Keras Model...")
        # Since Tensorflow can be heavy, we instantiate once on startup
        self.model = ChessZeroModel()
        self.mcts = MonteCarloTreeSearch(self.model, c_puct=1.0)
        logger.info("MCTS initialized.")

    async def GetPredictedMove(self, request, context):
        logger.info(f"Predicting move. is_white={request.is_white_turn}")
        
        state = request.bitboards_state
        bb = Bitboards(
            white_pawns=state.white_pawns,
            white_knights=state.white_knights,
            white_bishops=state.white_bishops,
            white_rooks=state.white_rooks,
            white_queens=state.white_queens,
            white_kings=state.white_kings,
            black_pawns=state.black_pawns,
            black_knights=state.black_knights,
            black_bishops=state.black_bishops,
            black_rooks=state.black_rooks,
            black_queens=state.black_queens,
            black_kings=state.black_kings
        )
        
        turn = Side.White if request.is_white_turn else Side.Black
        
        time_limit = float(os.getenv("ENGINE_TIME_LIMIT", "1.0"))
        logger.info(f"Running MCTS for {time_limit} seconds...")
        
        best_move = self.mcts.search(initial_bb=bb, turn=turn, time_limit=time_limit, temperature=0.1)
        
        if not best_move:
            logger.warning("No legal moves found! Returning empty UCI.")
            return chessai_pb2.PredictedMoveResponse(uci_move="")
            
        from_sq = index_to_square(best_move[0])
        to_sq = index_to_square(best_move[1])
        uci_move = f"{from_sq}{to_sq}"
        
        logger.info(f"Predicted move: {uci_move}")
        
        return chessai_pb2.PredictedMoveResponse(
            uci_move=uci_move
        )

async def serve():
    server = grpc.aio.server()
    chessai_pb2_grpc.add_AiServiceServicer_to_server(AiService(), server)
    
    port = os.getenv("PREDICTAPP_GRPC_PORT", "50053")
    server.add_insecure_port(f'[::]:{port}')
    
    logger.info(f"Starting predictapp AI gRPC server on port {port}")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
