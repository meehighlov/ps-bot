from sqlalchemy import Integer, Column, String

from ps_bot.database.entities.base import Base


class User(Base):

    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    user_role = Column(String(255))
    user_telegram_id = Column(Integer)
    user_telegram_username = Column(String(255))
