from pydantic import BaseModel


class CreateBoard(BaseModel):
    name: str
    game_format: str
    time: str
    additional: str