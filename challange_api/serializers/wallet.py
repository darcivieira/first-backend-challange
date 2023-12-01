from pydantic import BaseModel, Field
from challange_api.utils.dictionary import *


class WalletModel(BaseModel):
    value: float = Field(description=WALLET_FIELD_VALUE)


class WalletResponse(WalletModel):
    id: str = Field(description=FIELD_IDENTIFICATION)


class WalletCreate(WalletModel):
    value: float = Field(0.0, description=WALLET_FIELD_VALUE)
    user_id: str = Field(description=USER_FIELD_REGISTER_NUMBER)


class WalletUpdate(WalletModel):
    ...
