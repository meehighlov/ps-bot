from sqlalchemy import Column, String

from ps_bot.database.entities.base import Base


class Game(Base):

    __tablename__ = 'game'

    game_id = Column(String, primary_key=True)
    game_name = Column(String(255))
    game_description = Column(String(512))
