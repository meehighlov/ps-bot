import uuid

from sqlalchemy import select

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


@invoke_session
async def get_list_games(session) -> list[GameModel]:
    query = select(Game)
    result = await session.execute(query)
    return [GameModel.from_orm(game) for game in result.scalars().all()]
