import logging

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
)

from ps_bot.auth import auth
from ps_bot.database.queries.account import get_list_account
from ps_bot.exception import do_default_reply_on_any_error
from ps_bot.services.factories.factories import get_cryptography_password_utils

logger = logging.getLogger(__name__)

@auth
@do_default_reply_on_any_error
async def list_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cryptography_password_utils = get_cryptography_password_utils()
    accounts = await get_list_account()
    if accounts:
        message = "List of Accounts:\n\n"
        for idx, account in enumerate(accounts, 1):
            decrypted_password = cryptography_password_utils.decrypt(account.account_password)
            message += f"{idx}: Login: {account.account_login}, Password: {decrypted_password}\n"
    else:
        message = "No accounts found."

    await update.message.reply_text(message)


list_account_handler = CommandHandler(command='list_account', callback=list_account)
