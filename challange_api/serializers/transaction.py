from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

from challange_api.utils.dictionary import *


class TransactionType(str, Enum):
    wire_transfer = 'wire_transfer'
    bank_deposit = 'bank_deposit'


class TransactionStatus(str, Enum):
    pending = 'pending'
    success = 'success'
    failed = 'failed'


class TransactionModel(BaseModel):
    value: float = Field(description=TRANSACTION_FIELD_VALUE)


class TransactionCreate(TransactionModel):
    register_number: str = Field(description=USER_FIELD_REGISTER_NUMBER)


class TransactionCreateInDB(TransactionModel):
    receiver_id: str = Field(description=TRANSACTION_FIELD_RECEIVER_ID)
    sender_id: Optional[str] = Field(None, description=TRANSACTION_FIELD_SENDER_ID)
    status: TransactionStatus = Field(TransactionStatus.pending.value, description=TRANSACTION_FIELD_STATUS)
    type: TransactionType = Field(TransactionType.wire_transfer.value, description=TRANSACTION_FIELD_TYPE)


class TransactionUpdate(TransactionModel):
    receiver_id: str = Field(description=TRANSACTION_FIELD_RECEIVER_ID)
    sender_id: Optional[str] = Field(None, description=TRANSACTION_FIELD_SENDER_ID)
    status: TransactionStatus = Field(TransactionStatus.pending.value, description=TRANSACTION_FIELD_STATUS)
    type: TransactionType = Field(TransactionType.wire_transfer.value, description=TRANSACTION_FIELD_TYPE)


class TransactionResponse(TransactionUpdate):
    id: str = Field(description=FIELD_IDENTIFICATION)
