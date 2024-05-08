import uuid

from sqlalchemy import select
from ps_bot.database.entities.account import Account
from ps_bot.database.entities.enums import KeyCodeStatusEnum
from ps_bot.database.entities.game import Game
from ps_bot.database.entities.key_code import KeyCode
from ps_bot.database.session import invoke_session
from ps_bot.services.factories.factories import get_cryptography_password_utils


@invoke_session
async def save_account_to_db(session, data: dict) -> Account:
    cryptography_password_utils = get_cryptography_password_utils()
    encrypted_password = cryptography_password_utils.encrypt(data["password"])

    account = Account(
        account_id=str(uuid.uuid4()),
        account_login=data["login"],
        account_password=encrypted_password,
    )
    session.add(account)

    for code in data["codes"].split():
        key_code = KeyCode(
            key_code_id=str(uuid.uuid4()),
            key_code_status=KeyCodeStatusEnum.bound.value,
            key_code_value=code,
            account_id=account.account_id,
        )

        session.add(key_code)

    return account


@invoke_session
async def add_game_to_db(session, data: dict) -> Game:

    game = Game(
        game_id=str(uuid.uuid4()),
        name=data['name'],
        description=data['description'])

    session.add(game)

    return game


@invoke_session
async def get_list_account(session) -> list[Account]:
    result = await session.execute(select(Account))
    return result.scalars().all()
