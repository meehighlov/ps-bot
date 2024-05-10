from ps_bot.auth import auth
from ps_bot.database.queries.db_calls import add_game_to_db
from ps_bot.exception import do_default_reply_on_any_error
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from ps_bot.config import config
from ps_bot.handlers.enums import ButtonStatesEnum

ACCEPT_GAME_NAME = 4
ADD_GAME_DESCRIPTION = 5
END = -1


def build_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Сохранить 💾",
                callback_data=ButtonStatesEnum.ADD_GAME_SAVE,
            ),
            InlineKeyboardButton(
                text="Заполнить заново 🔁",
                callback_data=ButtonStatesEnum.ADD_GAME_RESTART,
            ),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup


@auth
@do_default_reply_on_any_error
async def add_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = (
        "Добавляем игру😎\n"
        "Введи название игры"
    )
    await update.message.reply_text(message)

    return ACCEPT_GAME_NAME


@do_default_reply_on_any_error
async def accept_game_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    game = update.message.text
    context.user_data["game"] = game

    message = (
        "Отлично! "
        f"Теперь введи описание для {game}"
    )
    await update.message.reply_text(message)

    return ADD_GAME_DESCRIPTION


@do_default_reply_on_any_error
async def add_description_for_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    description = update.message.text
    context.user_data["description"] = description

    game = context.user_data["game"]

    message = (
        "Отлично! проверь, все ли верно? 🤔\n\n"
        f"Название игры: {game}\n"
        f"Описание: {description}\n"
    )
    await update.message.reply_text(message, reply_markup=build_keyboard())

    return END


async def handle_button_save_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    context.user_data["user_id"] = update.effective_user.id
    await add_game_to_db(data=context.user_data)
    await update.effective_chat.send_message("Игра успешно добавлена ✅")

    # очищаем кеш, это важно сделать, чтобы не текла память
    context.user_data.clear()
    await query.edit_message_reply_markup(reply_markup=None)


async def handle_button_retry_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    await update.effective_chat.send_message("Нажми /add_game чтобы начать заново")

    # очищаем кеш, это важно сделать, чтобы не текла память
    context.user_data.clear()
    await query.edit_message_reply_markup(reply_markup=None)


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Это заглушка для либы, мы будем юзать декоратор do_default_reply_on_any_error
    pass


add_game_handler = ConversationHandler(
    entry_points=[CommandHandler("add_game", add_game)],
    states={
        ACCEPT_GAME_NAME: [MessageHandler(filters.TEXT, accept_game_name)],
        ADD_GAME_DESCRIPTION: [MessageHandler(filters.TEXT, add_description_for_game)]
    },
    fallbacks=[MessageHandler(filters.TEXT, fallback)],
    allow_reentry=False,
    conversation_timeout=config.bot.conversation_timeout_sec,
)

game_buttons = {
    ButtonStatesEnum.ADD_GAME_SAVE: handle_button_save_press,
    ButtonStatesEnum.ADD_GAME_RESTART: handle_button_retry_press,
}
