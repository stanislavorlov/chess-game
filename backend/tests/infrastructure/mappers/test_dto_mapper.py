import unittest
from datetime import datetime
from chessapp.infrastructure.mappers.dto_mapper import DtoMapper
from chessapp.domain.game.chess_game import ChessGame
from chessapp.domain.value_objects.game_id import ChessGameId
from chessapp.domain.players.players import Players
from chessapp.domain.value_objects.game_information import GameInformation
from chessapp.domain.value_objects.game_format import GameFormat
from chessapp.domain.chessboard.position import Position

class TestDtoMapperSan(unittest.TestCase):
    def test_map_game_calculates_san_on_the_fly(self):
        # Setup: Create a game and make some moves
        game_id = ChessGameId.generate_id()
        players = Players("white_user", "black_user")
        game_format = GameFormat.parse_string("rapid", "600s", "5s")
        info = GameInformation(game_format, datetime.now(), "Test Game")
        game = ChessGame.create(game_id, players, info)
        game.start()
        
        # Move 1: e2 -> e4
        from1 = Position.parse("e2")
        to1 = Position.parse("e4")
        p1 = game.get_board()[from1].piece
        game.move_piece(from1, to1, p1, None)
        
        # Move 2: e7 -> e5 (Black)
        from2 = Position.parse("e7")
        to2 = Position.parse("e5")
        p2 = game.get_board()[from2].piece
        game.move_piece(from2, to2, p2, None)
        
        # Act: Map the game to DTO
        dto = DtoMapper.map_game(game)
        
        # Assert: SAN should be present in history even though it's not in domain
        self.assertEqual(len(dto.history), 2)
        self.assertEqual(dto.history[0]['san'], "e4")
        self.assertEqual(dto.history[1]['san'], "e5")
        self.assertEqual(dto.history[0]['from'], "e2")
        self.assertEqual(dto.history[0]['to'], "e4")
        self.assertEqual(dto.history[1]['from'], "e7")
        self.assertEqual(dto.history[1]['to'], "e5")

    def test_map_game_calculates_time_on_the_fly(self):
        from unittest.mock import patch
        from chessapp.domain.value_objects.side import Side
        
        # Patch datetime inside ALL relevant modules from the start
        with patch('chessapp.domain.game.chess_game.datetime') as mock_game_dt, \
             patch('chessapp.domain.game.game_history.datetime') as mock_hist_dt, \
             patch('chessapp.infrastructure.mappers.dto_mapper.datetime') as mock_dto_dt:
            
            # Use a fixed start time
            start_date = datetime(2023, 1, 1, 12, 0, 0)
            mock_game_dt.now.return_value = start_date
            mock_hist_dt.now.return_value = start_date
            mock_dto_dt.now.return_value = start_date
            
            # Setup: 10m rapid game
            game_id = ChessGameId.generate_id()
            players = Players("white_user", "black_user")
            game_format = GameFormat.parse_string("rapid", "600s", "0s")
            info = GameInformation(game_format, start_date, "Test Time")
            game = ChessGame.create(game_id, players, info)
            
            # Game starts at 12:00:00
            game.start() 
            
            # Current time is 12:00:10 (10s elapsed since start, White's turn)
            mock_dto_dt.now.return_value = datetime(2023, 1, 1, 12, 0, 10)
            
            dto = DtoMapper.map_game(game)
            
            # White should have 590s remaining (600 - 10)
            self.assertEqual(dto.game_format.remaining_time, 590.0)
            self.assertEqual(dto.game_format.white_remaining_time, 590.0)
            self.assertEqual(dto.game_format.black_remaining_time, 600.0)
            
            # Now simulate a move by White at 12:00:10
            mock_game_dt.now.return_value = datetime(2023, 1, 1, 12, 0, 10)
            mock_hist_dt.now.return_value = datetime(2023, 1, 1, 12, 0, 10)
            
            from_pos = Position.parse("e2")
            to_pos = Position.parse("e4")
            piece = game.get_board()[from_pos].piece
            game.move_piece(from_pos, to_pos, piece, None)
            
            # After move, White's timer in Game object is not auto-updated 
            # (unless tick or reconstitution happens), but DtoMapper's 
            # projection should account for T10 - T0 = 10s consumption.
            # However, ChessGame reconstitution in __init__ DOES handle it.
            # For a live object, we rely on DtoMapper's projection.
            
            # Map again at 12:00:25 (15s elapsed since move at 12:00:10, Black's turn)
            mock_dto_dt.now.return_value = datetime(2023, 1, 1, 12, 0, 25)
            dto2 = DtoMapper.map_game(game)
            
            # Black's turn, black should have 585s remaining (600 - 15)
            # White should remain at 590 (until next move or tick)
            # Actually, with increment 0, it should be 590.
            self.assertEqual(dto2.game_format.remaining_time, 585.0)
            self.assertEqual(dto2.game_format.white_remaining_time, 590.0)
            self.assertEqual(dto2.game_format.black_remaining_time, 585.0)

if __name__ == "__main__":
    unittest.main()
