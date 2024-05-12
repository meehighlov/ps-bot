from functools import lru_cache

from cryptography.fernet import Fernet

from ps_bot.config import config
from ps_bot.utils.cryptography_password_utils import CryptographyPasswordUtils


@lru_cache
def get_cryptography_password_utils() -> CryptographyPasswordUtils:
    return CryptographyPasswordUtils(Fernet(key=config.bot.crypt_key))
