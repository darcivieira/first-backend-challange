from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from challange_api.generics.models import Model
from challange_api.models.transaction import Transaction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from challange_api.models import Users


class Wallet(Model):
    __tablename__ = 'wallet'

    value: Mapped[float] = mapped_column(DECIMAL)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="wallet", lazy='subquery')
    sender: Mapped["Transaction"] = relationship(back_populates="sender", foreign_keys="Transaction.sender_id", lazy='subquery')
    receiver: Mapped["Transaction"] = relationship(back_populates="receiver", foreign_keys="Transaction.receiver_id", lazy='subquery')

