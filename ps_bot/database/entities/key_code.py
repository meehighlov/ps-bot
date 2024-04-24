from sqlalchemy import Column, String

from ps_bot.database.entities.base import Base


class KeyCode(Base):

    __tablename__ = 'key_code'
    key_code_id = Column(String, primary_key=True)
    key_code_status = Column(String(255))
    key_code_value = Column(String(255))

    account_id = Column(String(255))
