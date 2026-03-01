import unittest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from chessapp.application.handlers.move_piece_handler import MovePieceHandler
from chessapp.application.commands.move_piece_command import MovePieceCommand
from chessapp.domain.game.chess_game import ChessGame
from chessapp.domain.value_objects.game_id import ChessGameId
from chessapp.domain.players.players import Players
from chessapp.domain.value_objects.game_information import GameInformation
from chessapp.domain.value_objects.game_format import GameFormat
from chessapp.domain.chessboard.position import Position

class TestMovePieceHandler(unittest.IsolatedAsyncioTestCase):
    async def test_handle_calculates_and_updates_san(self):
        # Setup
        game_id = ChessGameId.generate_id()
        players = Players("w", "b")
        game_format = GameFormat.parse_string("rapid", "10m", "5s")
        info = GameInformation(game_format, datetime.now(), "Test")
        game = ChessGame.create(game_id, players, info)
        game.start()
        
        repo = AsyncMock()
        repo.find.return_value = game
        mediator = AsyncMock()
        logger = MagicMock()
        
        handler = MovePieceHandler(repo, mediator, logger)
        
        from_pos = Position.parse("e2")
        to_pos = Position.parse("e4")
        piece = game.get_board()[from_pos].piece
        
        command = MovePieceCommand(
            game_id=game_id,
            from_=from_pos,
            to=to_pos,
            piece=piece,
            captured=None
        )
        
        # Act
        await handler.handle(command)
        
        # Assert
        last_entry = game.history.last()
        self.assertIsNotNone(last_entry)
        repo.save.assert_called_once_with(game)
        mediator.dispatch_events.assert_called_once_with(game)

if __name__ == "__main__":
    unittest.main()
