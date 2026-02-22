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

if __name__ == "__main__":
    unittest.main()
