from typing import Callable

from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

from ps_bot.handlers.enums import ButtonStatesEnum


def button_press_handler(button_handlers: dict[ButtonStatesEnum, Callable]) -> CallbackQueryHandler:
    async def on_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query

        handler = button_handlers[ButtonStatesEnum(query.data)]

        await handler(update=update, context=context)

    return CallbackQueryHandler(on_button_press)
