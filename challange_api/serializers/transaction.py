from enum import Enum
from typing import Optional
from pydantic import BaseModel


class TransactionType(str, Enum):
    wire_transfer = 'wire_transfer'
    bank_deposit = 'bank_deposit'


class TransactionStatus(str, Enum):
    pending = 'pending'
    success = 'success'
    failed = 'failed'


class TransactionModel(BaseModel):
    value: float


class TransactionCreate(TransactionModel):
    register_number: str


class TransactionCreateInDB(TransactionModel):
    receiver_id: str
    sender_id: Optional[str] = None
    status: TransactionStatus = TransactionStatus.pending.value
    type: TransactionType = TransactionType.wire_transfer.value


class TransactionUpdate(TransactionModel):
    receiver_id: str
    sender_id: Optional[str] = None
    status: TransactionStatus = TransactionStatus.pending
    type: TransactionType = TransactionType.wire_transfer


class TransactionResponse(TransactionUpdate):
    id: str
