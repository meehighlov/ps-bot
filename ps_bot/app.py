import logging
import subprocess
from typing import TYPE_CHECKING, List

from telegram.ext import ApplicationBuilder, DictPersistence

from ps_bot.config import config, BASE_DIR

if TYPE_CHECKING:
    from telegram.ext import Application
    from telegram.ext import BaseHandler


def create_app(handlers: List['BaseHandler']) -> 'Application':

    if config.bot.run_migrations:
        result = subprocess.run(
            f"cd {BASE_DIR} && alembic upgrade head",
            shell=True,
            check=True,
        )

        if result.returncode != 0:
            raise Exception(f"Error running migrations. {result.stderr}, {result.stdout}")

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
