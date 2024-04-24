"""init

Revision ID: 35534a69f059
Revises: 
Create Date: 2024-04-26 00:54:09.129088

"""
from typing import Sequence, Union

import sqlite3

from ps_bot.config import config

# revision identifiers, used by Alembic.
revision: str = '35534a69f059'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


upgrade_script = '''

CREATE TABLE account (
    account_id TEXT PRIMARY KEY,
    account_login TEXT NOT NULL,
    account_password TEXT NOT NULL,
    game_id INTEGER NOT NULL
);

CREATE TABLE game (
    game_id TEXT PRIMARY KEY,
    game_name TEXT NOT NULL,
    game_description TEXT
);

CREATE TABLE user (
    user_id TEXT PRIMARY KEY,
    user_role TEXT NOT NULL,
    user_telegram_id INTEGER,
    user_telegram_username TEXT
);

CREATE TABLE key_code (
    key_code_id TEXT PRIMARY KEY,
    key_code_status TEXT NOT NULL,
    key_code_value TEXT NOT NULL,
    account_id TEXT NOT NULL
);
'''

downgrade_script = '''

DROP TABLE account;
DROP TABLE game;
DROP TABLE user;
DROP TABLE key_code;
'''


def upgrade() -> None:
    conn = sqlite3.connect(config.db.sqlite_path)
    cur = conn.cursor()

    cur.executescript(upgrade_script)
    cur.connection.commit()
    cur.connection.close()


def downgrade() -> None:
    conn = sqlite3.connect(config.db.sqlite_path)
    cur = conn.cursor()

    cur.executescript(downgrade_script)
    cur.connection.commit()
    cur.connection.close()
