import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f'handling start command for user_id = {update.effective_user.id}')
    await update.message.reply_text(f'Привет, {update.effective_user.first_name} 👋')


start_handler = CommandHandler(command='start', callback=start)
