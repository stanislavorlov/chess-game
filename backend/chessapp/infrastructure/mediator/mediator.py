from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable
from ...application.handlers.base_command_handler import BaseCommandHandler, CT, RT as CR
from ...application.handlers.base_event_handler import BaseEventHandler, ET, RT as ER
from ...application.handlers.base_query_handler import BaseQueryHandler, QT, RT as QR
from ...infrastructure.mediator.exceptions import NoHandlerRegisteredException


@dataclass(eq=False, init=False)
class Mediator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Mediator, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance

    def __init__(self) -> None:
        self._commands_map: defaultdict[CT, list[BaseCommandHandler]] = defaultdict(list)
        self._query_map: defaultdict[QT, list[BaseQueryHandler]] = defaultdict(list)
        self._events_map: defaultdict[ET, list[BaseEventHandler]] = defaultdict(list)

    def reset(self) -> None:
        self._commands_map: defaultdict[CT, list[BaseCommandHandler]] = defaultdict(list)
        self._query_map: defaultdict[QT, list[BaseQueryHandler]] = defaultdict(list)
        self._events_map: defaultdict[ET, list[BaseEventHandler]] = defaultdict(list)

    def register_command(self, command: CT, handlers: Iterable[BaseCommandHandler]) -> None:
        self._commands_map[command].extend(handlers)

    def register_event(self, event: ET, handlers: Iterable[BaseEventHandler]) -> None:
        self._events_map[event].extend(handlers)

    def register_query(self, query: QT, handlers: Iterable[BaseQueryHandler]) -> None:
        self._query_map[query].extend(handlers)

    async def handle_command(self, command: CT) -> Iterable[CR]:
        handlers: list[BaseCommandHandler] = self._commands_map[command.__class__]

        if not handlers:
            raise NoHandlerRegisteredException(f'No handler registered for {command.__class__}')
        return [await handler.handle(command) for handler in handlers]

    async def handle_event(self, event: ET) -> Iterable[ER]:
        handlers: list[BaseEventHandler] = self._events_map[event.__class__]

        if not handlers:
            # Optionally log that no handler is registered for the event
            return []
        return [await handler.handle(event) for handler in handlers]

    async def dispatch_events(self, aggregate_root):
        """Dispatches all domain events from an aggregate and clears them."""
        events = list(aggregate_root.domain_events)
        aggregate_root.domain_events.clear()
        
        for event in events:
            await self.handle_event(event)

    async def handle_query(self, query: QT) -> Iterable[QR]:
        handlers: list[BaseQueryHandler] = self._query_map[query.__class__]

        if not handlers:
            raise NoHandlerRegisteredException(f'No handler registered for {query.__class__}')
        return [await handler.handle(query) for handler in handlers]