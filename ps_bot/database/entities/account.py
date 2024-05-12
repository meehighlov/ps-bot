from sqlalchemy import Column, String

from ps_bot.database.entities.base import Base


class Account(Base):

    __tablename__ = 'account'

    account_id = Column(String, primary_key=True)
    account_login = Column(String(255))
    account_password = Column(String(255))

    game_id = Column(String(255), default='')
