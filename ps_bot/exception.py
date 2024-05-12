import logging
from functools import wraps

from telegram import Update


logger = logging.getLogger(__name__)


def do_default_reply_on_any_error(command_handler):

    @wraps(command_handler)
    async def handle(update: Update, context):
        try:
            return await command_handler(update, context)
        except Exception as e:
            user_id = update.effective_user.id
            username = update.effective_user.username  # may be empty if user have private settings
            logger.error(
                f"Error occurred for user with id {user_id} and username {username}, "
                f"Original error was: {e}"
            )

            message = (
                "Извиняюсь, я не смог разобрать твой запрос😔\n"
                "Проверь, пожайлуста, запрос и попробуй снова🙏\n"
                "Если твой запрос корректен, вероятно, возникла непредвиденная ошибка"
            )
            await update.effective_user.send_message(text=message)

        return

    return handle
