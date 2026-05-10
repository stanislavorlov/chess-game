from beanie import Document


class PlayerDocument(Document):
    name: str
    rank: int
    games_history: []

    class Config:
        pass

    class Settings:
        name = "players"

class GameHistory:
    game_id: str
    result: str