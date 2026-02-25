import unittest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime
from chessapp.interface.main import app
from chessapp.infrastructure.mediator.container import get_mediator
from chessapp.application.dtos.chess_game_dto import ChessGameDto, GameStateDto, GameFormatDto, PlayersDto

class TestGameApi(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.mock_mediator = AsyncMock()
        
        # Override dependency
        app.dependency_overrides[get_mediator] = lambda: self.mock_mediator

    def tearDown(self):
        app.dependency_overrides = {}

    def test_get_board_contract(self):
        # Prepare a mock DTO that represents what the backend returns
        mock_dto = ChessGameDto(
            game_id="65b2a1e1f1d1e1f1d1e1f1d1",
            moves_count=0,
            date=datetime.now(),
            name="Test Game",
            status="started",
            state=GameStateDto(
                turn="white",
                started=True,
                finished=False,
                check_side=None,
                check_position=None,
                legal_moves=[]
            ),
            game_format=GameFormatDto(
                value="10+5",
                white_remaining_time=600.0,
                black_remaining_time=600.0,
            ),
            players=PlayersDto(
                white_id="white_user",
                black_id="black_user"
            ),
            board=[
                {
                    "square": "e2",
                    "piece": {"abbreviation": "P", "moved": False},
                    "color": "white",
                    "rank": 2
                }
            ],
            history=[
                {
                    "sequence": 1,
                    "piece": {"abbreviation": "P", "moved": True},
                    "from": "e2",
                    "to": "e4",
                    "san": "e4",
                    "action_type": "PieceMoved"
                }
            ]
        )
        
        self.mock_mediator.handle_query.return_value = [mock_dto]
        
        response = self.client.get("/api/game/board/65b2a1e1f1d1e1f1d1e1f1d1")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()["data"]
        self._verify_dto_contract(data)

    def test_create_board_contract(self):
        # Prepare a mock DTO
        mock_dto = ChessGameDto(
            game_id="65b2a1e1f1d1e1f1d1e1f1d1",
            moves_count=0,
            date=datetime.now(),
            name="New Game",
            status="created",
            state=GameStateDto(
                turn="white",
                started=False,
                finished=False,
                check_side=None,
                check_position=None,
                legal_moves=[]
            ),
            game_format=GameFormatDto(
                value="10+5",
                white_remaining_time=600.0,
                black_remaining_time=600.0,
            ),
            players=PlayersDto(
                white_id="",
                black_id=""
            ),
            board=[],
            history=[]
        )
        
        self.mock_mediator.handle_command.return_value = [mock_dto]
        
        payload = {
            "name": "New Game",
            "game_format": "rapid",
            "time": "600s",
            "additional": "5s"
        }
        
        response = self.client.post("/api/game/create_board/", json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json().get("data")
        
        self.assertIsNotNone(data)
        self._verify_dto_contract(data)

    def _verify_dto_contract(self, data):
        # Contract Verification (matches frontend ChessGameDto)
        self.assertIn("game_id", data)
        self.assertIn("moves_count", data)
        self.assertIn("date", data)
        self.assertIn("name", data)
        self.assertIn("state", data)
        self.assertIn("game_format", data)
        self.assertIn("players", data)
        self.assertIn("board", data)
        self.assertIn("history", data)
        
        # Verify state properties
        state = data["state"]
        self.assertIn("turn", state)
        self.assertIn("started", state)
        self.assertIn("finished", state)
        self.assertIn("check_side", state)
        self.assertIn("check_position", state)
        self.assertIn("legal_moves", state)

if __name__ == "__main__":
    unittest.main()
