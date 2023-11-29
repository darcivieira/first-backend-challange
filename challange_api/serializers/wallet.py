from pydantic import BaseModel


class WalletModel(BaseModel):
    value: float


class WalletResponse(WalletModel):
    id: str


class WalletCreate(WalletModel):
    value: float = 0.0
    user_id: str


class WalletUpdate(WalletModel):
    ...
