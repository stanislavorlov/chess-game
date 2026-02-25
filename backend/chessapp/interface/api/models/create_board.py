from pydantic import BaseModel


class CreateBoard(BaseModel):
    name: str
    format: str
    time: str
    increment: str