import logging
from typing import TYPE_CHECKING, List

from telegram.ext import ApplicationBuilder, DictPersistence

from ps_bot.config import config

if TYPE_CHECKING:
    from telegram.ext import Application
    from telegram.ext import BaseHandler


def create_app(handlers: List['BaseHandler']) -> 'Application':

    persistence = DictPersistence()
    app = (
        ApplicationBuilder()
        .token(config.bot.token)
        .persistence(persistence)
        .build()
    )

    for handler in handlers:
        app.add_handler(handler)

    logging.basicConfig(
        filename='logs.log',
        encoding='utf-8',
        level=logging.DEBUG,
    )

    return app
