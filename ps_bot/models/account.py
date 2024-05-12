from pydantic import BaseModel


class AccountModel(BaseModel):
    """Account model.

    All fields are taken from Account orm model.
    """

    account_id: str
    account_login: str
    account_password: str
    game_id: str | None

    class Config:
        from_attributes = True
