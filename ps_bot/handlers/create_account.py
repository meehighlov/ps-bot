import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from ps_bot.auth import auth
from ps_bot.config import config
from ps_bot.database.queries.account import save_account_to_db

from ps_bot.exception import do_default_reply_on_any_error
from ps_bot.handlers.enums import ButtonStatesEnum

logger = logging.getLogger(__name__)


ACCEPT_LOGIN = 1
ACCEPT_PASSWORD = 2
ACCEPT_CODES = 3
END = -1


@auth
@do_default_reply_on_any_error
async def create_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    message = (
        "Добавляем аккаунт😎\n"
        "Введи логин аккаунта ps-store"
    )
    await update.message.reply_text(message)

    return ACCEPT_LOGIN


@do_default_reply_on_any_error
async def accept_login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    login = update.message.text

    context.user_data["login"] = login

    message = (
        "Отлично! "
        f"Теперь введи пароль аккаунта ps-store для {login}"
    )
    await update.message.reply_text(message)

    return ACCEPT_PASSWORD


@do_default_reply_on_any_error
async def accept_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    password = update.message.text

    context.user_data["password"] = password

    message = (
        "Логин и пароль есть, теперь передай через пробел коды для аккаунта😃"
    )
    await update.message.reply_text(message)

    return ACCEPT_CODES


def build_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Сохранить 💾",
                callback_data=ButtonStatesEnum.CREATE_ACCOUNT_SAVE,
            ),
            InlineKeyboardButton(
                text="Заполнить заново 🔁",
                callback_data=ButtonStatesEnum.CREATE_ACCOUNT_RESTART,
            ),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup


@do_default_reply_on_any_error
async def accept_codes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    codes = update.message.text

    context.user_data["codes"] = codes

    login = context.user_data["login"]
    password = context.user_data["password"]

    message = (
        "Отлично! проверь, все ли верно? 🤔\n\n"
        f"Создаем аккаунт\n\n"
        f"Логин: {login}\n"
        f"Пароль: {password}\n"
        f"Коды доступа: {codes}\n"
    )
    await update.message.reply_text(message, reply_markup=build_keyboard())

    return END


async def handle_button_save_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    context.user_data["user_id"] = update.effective_user.id
    await save_account_to_db(data=context.user_data)
    await update.effective_chat.send_message("Аккаунт создан ✅")

    # очищаем кеш, это важно сделать, чтобы не текла память
    context.user_data.clear()
    await query.edit_message_reply_markup(reply_markup=None)


async def handle_button_retry_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    await update.effective_chat.send_message("Нажми /create_account чтобы начать заново")

    # очищаем кеш, это важно сделать, чтобы не текла память
    context.user_data.clear()
    await query.edit_message_reply_markup(reply_markup=None)


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Это заглушка для либы, мы будем юзать декоратор do_default_reply_on_any_error
    pass


create_account_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("create_account", create_account)],
    states={
        ACCEPT_LOGIN: [MessageHandler(filters.TEXT, accept_login)],
        ACCEPT_PASSWORD: [MessageHandler(filters.TEXT, accept_password)],
        ACCEPT_CODES: [MessageHandler(filters.TEXT, accept_codes)],
    },
    fallbacks=[MessageHandler(filters.TEXT, fallback)],
    allow_reentry=False,
    conversation_timeout=config.bot.conversation_timeout_sec,
)

account_buttons = {
    ButtonStatesEnum.CREATE_ACCOUNT_SAVE: handle_button_save_press,
    ButtonStatesEnum.CREATE_ACCOUNT_RESTART: handle_button_retry_press,
}
