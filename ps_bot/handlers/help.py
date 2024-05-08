from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from ps_bot.config import config


async def help_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = ["))"]
    if update.effective_user.username in config.bot.owners:
        message = [
            'Доступные команды:', '\n\n',
            '/create_account', '\n'
            '/add_game', '\n'
            '/list_account',
        ]

    message = "".join(message)

    await update.message.reply_text(message)


help_handler = CommandHandler(command='help', callback=help_)
