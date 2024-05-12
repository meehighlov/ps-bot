from enum import Enum
from pathlib import Path

from pydantic.v1 import BaseSettings


BASE_DIR = Path(__file__).parents[1]
ENV_FILE = BASE_DIR / '.env'


class EnvName(Enum):
    local = 'local'
    prod = 'prod'


class LogLevel(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'


class BotConfig(BaseSettings):

    class Config:
        env_file = ENV_FILE
        env_prefix = 'BOT_'

    token: str
    loglevel: LogLevel = LogLevel.DEBUG.value
    env_name: EnvName = EnvName.local.value
    owners: list[str]
    conversation_timeout_sec: int = 120
    crypt_key: str
    run_migrations: bool = True


class DBConfig(BaseSettings):

    class Config:
        env_file = ENV_FILE
        env_prefix = 'DB_'

    sqlite_name: str

    @property
    def sqlite_path(self) -> str:
        return str(BASE_DIR / self.sqlite_name)


class Config(BaseSettings):

    bot: BotConfig
    db: DBConfig

    @classmethod
    def build(cls):
        return Config(
            bot=BotConfig(),
            db=DBConfig(),
        )


config = Config.build()
