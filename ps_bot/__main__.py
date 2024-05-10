import logging

from ps_bot.app import create_app
from ps_bot.handlers.games.add_game import game_buttons, add_game_handler
from ps_bot.handlers.buttons import button_press_handler
from ps_bot.handlers.create_account import account_buttons, create_account_conversation_handler
from ps_bot.handlers.games.get_list_games import get_list_games_handler
from ps_bot.handlers.help import help_handler
from ps_bot.handlers.start import start_handler

logger = logging.getLogger(__name__)

button_handlers = {
    **account_buttons,
    **game_buttons,
}

handlers = [
    start_handler,
    create_account_conversation_handler,
    help_handler,
    add_game_handler,
    button_press_handler(button_handlers=button_handlers),
    get_list_games_handler
]

app = create_app(handlers=handlers)

logger.info('Bot is ready, run polling')

app.run_polling()
