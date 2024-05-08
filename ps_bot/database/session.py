import logging
from functools import wraps
from typing import Callable

from sqlalchemy.ext.asyncio import create_async_engine

from ps_bot.config import config

from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
)


logger = logging.getLogger(__name__)


_engine = create_async_engine(f"sqlite+aiosqlite:///{config.db.sqlite_path}", echo=True)

async_session_factory = async_sessionmaker(
    _engine,
    expire_on_commit=False,
)
AsyncScopedSession = async_scoped_session(
    async_session_factory,
    scopefunc=current_task,
)


def invoke_session(func: Callable):
    """
    Async session control decorator.

    :param func: function which makes db call.
    :return: function call result
    """

    @wraps(invoke_session)
    async def wrapper(*args, **kwargs):
        scoped_session = AsyncScopedSession()

        try:
            result = await func(*args, session=scoped_session, **kwargs)
            await scoped_session.commit()
            return result
        except Exception as e:
            logger.info(f'Exception occurred {e}, rolling back...')
            await scoped_session.rollback()
            logger.info(f'Transaction rolled back.')
            raise
        finally:
            await scoped_session.close()

    return wrapper
