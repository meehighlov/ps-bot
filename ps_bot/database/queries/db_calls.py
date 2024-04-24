import uuid

from cryptography.fernet import Fernet

from ps_bot.config import config
from ps_bot.database.entities.account import Account
from ps_bot.database.entities.enums import KeyCodeStatusEnum
from ps_bot.database.entities.key_code import KeyCode
from ps_bot.database.session import invoke_session


@invoke_session
async def save_account_to_db(session, data: dict) -> Account:
    fernet = Fernet(config.bot.crypt_key.encode())
    password = fernet.encrypt(data["password"].encode())

    account = Account(
        account_id=str(uuid.uuid4()),
        account_login=data["login"],
        account_password=password.decode(),
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
