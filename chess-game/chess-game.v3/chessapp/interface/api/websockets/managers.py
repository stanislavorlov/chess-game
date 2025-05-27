import asyncio
from abc import abstractmethod, ABC
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from starlette.websockets import WebSocket


class BaseConnectionManager:
    #def __init__(self):
    #    self.connections_map: dict[str, list[WebSocket]] = defaultdict(list)

    @abstractmethod
    async def accept_connection(self, websocket: WebSocket, key: str): ...

    @abstractmethod
    async def remove_connection(self, websocket: WebSocket, key: str): ...

    @abstractmethod
    async def send_all(self, key: str, message: str): ...           # bytes_: bytes

    @abstractmethod
    async def disconnect_all(self, key: str): ...

#@dataclass
class ConnectionManager(BaseConnectionManager):
    # https://github.com/AlexanderLukash/fastapi-websocket-chat-kafka/blob/main/app/infra/websockets/managers.py#L17

    def __init__(self):
        super().__init__()
        self.lock_map: dict[str, asyncio.Lock] = defaultdict()
        self.connections_map: dict[str, list[WebSocket]] = defaultdict(list)
        print('ConnectionManager init')

    # def __post_init__(self):
    #     self.lock_map: dict[str, asyncio.Lock] = field(default_factory=dict)
    #
    #     self.connections_map: dict[str, list[WebSocket]] = field(
    #         default_factory=lambda: defaultdict(list),
    #         kw_only=True,
    #     )

    async def accept_connection(self, websocket: WebSocket, key: str):
        await websocket.accept()

        print('accept connection')
        print(id(self))
        print(websocket)

        if key not in self.lock_map:
            self.lock_map[key] = asyncio.Lock()

        async with self.lock_map[key]:
            self.connections_map[key].append(websocket)

        print(self.lock_map[key])
        print(self.connections_map[key])

    async def remove_connection(self, websocket: WebSocket, key: str):
        async with self.lock_map[key]:
            self.connections_map[key].remove(websocket)

    async def send_all(self, key: str, message: str):       # bytes_: bytes
        print('socket manager: send_all')
        print(id(self))
        print(self.lock_map)
        print(self.connections_map)
        for websocket in self.connections_map[key]:
            #await websocket.send_bytes(bytes_)
            await websocket.send_text(message)

    async def disconnect_all(self, key: str):
        lock = self.lock_map.get(key)

        if lock is None:
            return

        async with self.lock_map[key]:
            for websocket in self.connections_map[key]:
                await websocket.send_json(
                    {
                        "message": "Chat has been deleted.",
                    },
                )
                await websocket.close()