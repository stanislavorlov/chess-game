from pydantic import BaseModel


class CreateBoard(BaseModel):
    game_format: str
    time: str
    additional: str