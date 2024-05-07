import logging

from ps_bot.app import create_app
from ps_bot.handlers import (
    start_handler,
    create_account_buttons_handler,
    create_account_conversation_handler,
    help_handler,
    add_game_handler,
    add_game_buttons_handler
)

logger = logging.getLogger(__name__)

handlers = [
    start_handler,
    create_account_buttons_handler,
    create_account_conversation_handler,
    help_handler,
    add_game_handler,
    add_game_buttons_handler
]

app = create_app(handlers=handlers)

logger.info('Bot is ready, run polling')

app.run_polling()
