from pydantic import BaseModel


class GameModel(BaseModel):
    """Game model.

    All fields are taken from Game orm model.
    """

    game_id: str
    game_name: str
    game_description: str

    class Config:
        from_attributes = True
