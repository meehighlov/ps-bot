import uuid

from ps_bot.database.entities.game import Game
from ps_bot.database.session import invoke_session
from ps_bot.models.game import GameModel


@invoke_session
async def add_game_to_db(session, data: dict) -> GameModel:

    game = Game(
        game_id=str(uuid.uuid4()),
        game_name=data['name'],
        game_description=data['description'],
    )

    session.add(game)

    return GameModel.from_orm(game)
