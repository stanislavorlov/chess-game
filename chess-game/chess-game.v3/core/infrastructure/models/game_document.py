from beanie import Document

class GameDocument(Document):
    name: str
    status: str

    class Config:
        pass

    class Settings:
        # the name of the collection
        name = "games"