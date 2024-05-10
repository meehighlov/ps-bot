import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from ps_bot.database.queries.db_calls import get_list_games

logger = logging.getLogger(__name__)


async def get_games_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    games = await get_list_games()
    _games = []
    if games:
        _games.append("Все игры ps-store:\n\n")
        for idx, game in enumerate(games, 1):
            _games.append(f"{idx}: Логин: {game.game_name}, Пароль: {game.game_description}\n")
    else:
        _games.append("Нет игр в ps-store.")

    await update.message.reply_text("".join(_games))


get_list_games_handler = CommandHandler(command='get_games_list', callback=get_games_list)
