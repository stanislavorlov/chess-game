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
from ..domain.pieces.piece_factory import PieceFactory
from ..domain.value_objects.game_id import ChessGameId
from ..domain.value_objects.piece_id import PieceId
from ..domain.value_objects.side import Side
from ..infrastructure import models
from ..infrastructure.config.config import Settings
from ..infrastructure.mediator.container import get_mediator, get_connection_manager, get_repository, get_logger, \
    get_kafka_service
from ..infrastructure.services.kafka_service import KafkaService
from ..infrastructure.services.redis_service import RedisService
from ..interface.api.routes import game_api, move_api, piece_api
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
    kafka_service: KafkaService = app.state.kafka
    
    # Manually get dependencies since we're outside a request context
    repo = get_repository()
    settings = Settings()
    redis = RedisService(settings)
    logger_ = get_logger()
    mediator = get_mediator(repo, redis, logger_)

    logger.info("Starting Kafka Command Consumer...")
    try:
        async for command_data in kafka_service.consume_messages("chess-commands", group_id="chess-command-processors"):
            try:
                piece_id = PieceId(command_data['piece']['_id'])
                side = Side.black()
                if command_data['piece']['_side']['_value'] == 'W':
                    side = Side.white()

                command = MovePieceCommand(
                    game_id=ChessGameId(PydanticObjectId(command_data['game_id'])),
                    from_=Position.parse(command_data['from']),
                    to=Position.parse(command_data['to']),
                    piece=PieceFactory.create(piece_id, side, command_data['piece']['_type'])
                )
                logger.info(f"Consuming command from Kafka: {command}")
                await mediator.handle_command(command)
            except Exception as e:
                logger.error(f"Error processing Kafka command: {e}")
    except asyncio.CancelledError:
        logger.info("Kafka consumer task cancelled")
    except Exception as e:
        logger.error(f"Kafka consumer crashed: {e}")

async def subscribe_redis_notifications(app: FastAPI):
    redis_service: RedisService = app.state.redis
    connection_manager = get_connection_manager()

    logger.info("Starting Redis Notification Subscriber...")
    try:
        async for message in redis_service.subscribe("chess-notifications:*"):
            try:
                # message is a JSON string
                data = json.loads(message)
                game_id = data.get('game_id')
                if game_id:
                    logger.debug(f"Broadcasting Redis message to local sockets for game {game_id}")
                    await connection_manager.send_all(str(game_id), message)
            except Exception as e:
                logger.error(f"Error processing Redis notification: {e}")
    except asyncio.CancelledError:
        logger.info("Redis subscriber task cancelled")
    except Exception as e:
        logger.error(f"Redis subscriber crashed: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    client = AsyncIOMotorClient(settings.MONGO_HOST)
    await init_beanie(
        database=client.get_database(settings.MONGO_DB),
        document_models=models.__all__
    )

    app.state.redis = RedisService(settings)
    app.state.kafka = KafkaService(settings)
    
    # Start background tasks
    kafka_task = asyncio.create_task(consume_kafka_commands(app))
    redis_task = asyncio.create_task(subscribe_redis_notifications(app))

    yield

    # Cancellation of background tasks
    kafka_task.cancel()
    redis_task.cancel()
    
    # Wait for tasks to clean up
    await asyncio.gather(kafka_task, redis_task, return_exceptions=True)
    
    await app.state.kafka.stop_all()
    await app.state.redis.disconnect()
    client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(game_api.router)
app.include_router(move_api.router)
app.include_router(piece_api.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
            
            # Produce to Kafka for durable processing
            await kafka_service.send_message("chess-commands", message_data)
            logger.info("Command produced to Kafka successfully")

    except WebSocketDisconnect:
        await connection_manager.remove_connection(websocket, game_id)
    except Exception as e:
        logger.error(f"WebSocket error in {game_id}: {e}")
        await connection_manager.remove_connection(websocket, game_id)
