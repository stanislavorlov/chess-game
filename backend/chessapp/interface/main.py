import asyncio
import json
import logging
from contextlib import asynccontextmanager
from typing import Annotated
from beanie import PydanticObjectId, init_beanie
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from ..application.commands.move_piece_command import MovePieceCommand
from ..domain.chessboard.position import Position
from ..domain.events.piece_move_failed import PieceMoveFailed
from ..domain.value_objects.game_id import ChessGameId
from ..infrastructure import models
from ..infrastructure.config.config import Settings
from ..infrastructure.mediator.container import get_mediator, get_connection_manager, get_repository, get_logger, \
    get_kafka_service
from ..infrastructure.services.kafka_service import KafkaService
from ..infrastructure.services.redis_service import RedisService
from ..interface.api.routes import game_api
from ..interface.api.websockets.managers import ConnectionManager

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True,
)
logger = logging.getLogger("chessapp")

# Silence noisy third-party logs
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("motor").setLevel(logging.WARNING)
logging.getLogger("aiokafka").setLevel(logging.WARNING)


async def consume_kafka_commands(app: FastAPI):
    try:
        kafka_service: KafkaService = app.state.kafka
        
        # Manually get dependencies since we're outside a request context
        repo = get_repository()
        settings = Settings()
        redis = RedisService(settings)
        logger_ = get_logger()
        mediator = get_mediator(repo, redis, logger_)

        async for command_data in kafka_service.consume_messages("chess-commands", group_id="chess-command-processors"):
            try:
                # Command data now only needs game_id, from, to
                command = MovePieceCommand(
                    game_id=ChessGameId(PydanticObjectId(command_data['game_id'])),
                    from_=Position.parse(command_data['from']),
                    to=Position.parse(command_data['to'])
                )
                logger.info(f"Consuming command from Kafka: {command}")
                await mediator.handle_command(command)
            except Exception as e:
                logger.error(f"Error processing Kafka command: {e}")
                # Report failure back to client via Redis
                try:
                    game_id_str = command_data.get('game_id')
                    if game_id_str:
                        failure_event = {
                            "event_type": "piece-move-failed",
                            "game_id": game_id_str,
                            "reason": f"Server error: {str(e)}",
                            "from_": command_data.get('from'),
                            "to": command_data.get('to')
                        }
                        await redis.publish(f"chess-notifications:{game_id_str}", json.dumps(failure_event))
                except Exception as redis_err:
                    logger.error(f"Failed to publish error to Redis: {redis_err}")
    except asyncio.CancelledError:
        logger.info("Kafka consumer task cancelled")
    except Exception as e:
        logger.error(f"Kafka consumer crashed: {e}")

async def subscribe_redis_notifications(app: FastAPI):
    redis_service: RedisService = app.state.redis
    connection_manager = get_connection_manager()

    try:
        async for message in redis_service.subscribe("chess-notifications:*"):
            try:
                # message is a JSON string
                data = json.loads(message)
                game_id = data.get('game_id')
                if game_id:
                    await connection_manager.send_all(str(game_id), message)
            except Exception as e:
                logger.error(f"Error processing Redis notification: {e}")
    except asyncio.CancelledError:
        logger.info("Redis subscriber task cancelled")
    except Exception as e:
        logger.error(f"Redis subscriber crashed: {e}")

@asynccontextmanager
async def lifespan(_app: FastAPI):
    settings = Settings()
    client = AsyncIOMotorClient(settings.MONGO_HOST)
    
    try:
        await init_beanie(
            database=client.get_database(settings.MONGO_DB),
            document_models=models.__all__
        )
    except Exception as e:
        raise

    _app.state.redis = RedisService(settings)
    _app.state.kafka = KafkaService(settings)
    
    # Start background tasks
    kafka_task = asyncio.create_task(consume_kafka_commands(_app))
    redis_task = asyncio.create_task(subscribe_redis_notifications(_app))

    yield

    # Cancellation of background tasks
    kafka_task.cancel()
    redis_task.cancel()
    
    # Wait for tasks to clean up
    await asyncio.gather(kafka_task, redis_task, return_exceptions=True)
    
    await _app.state.kafka.stop_all()
    await _app.state.redis.disconnect()
    client.close()


def create_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)

    _app.include_router(game_api.router)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app

app = create_app()

@app.websocket("/ws/{game_id}")
async def websocket_endpoint(
        game_id: str,
        websocket: WebSocket,
        connection_manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
        kafka_service: Annotated[KafkaService, Depends(get_kafka_service)]
):
    await connection_manager.accept_connection(websocket=websocket, key=game_id)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Websocket message received for game {game_id}: {data}")
            
            message_data = json.loads(data)
            message_data['game_id'] = game_id # Ensure game_id is present
            
            try:
                # Produce to Kafka for durable processing
                await kafka_service.send_message("chess-commands", message_data)
                logger.info("Command produced to Kafka successfully")
            except Exception as e:
                logger.error(f"Failed to produce to Kafka: {e}")
                # Immediate feedback if local production fails
                await websocket.send_text(json.dumps({
                    "event_type": PieceMoveFailed.event_type,
                    "game_id": game_id,
                    "reason": "Connection error: Failed to queue move",
                    "from_": message_data.get('from'),
                    "to": message_data.get('to')
                }))

    except WebSocketDisconnect:
        await connection_manager.remove_connection(websocket, game_id)
    except Exception as e:
        logger.error(f"WebSocket error in {game_id}: {e}")
        await connection_manager.remove_connection(websocket, game_id)
