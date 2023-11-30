from sqlalchemy import DECIMAL, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from challange_api.generics.models import Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from challange_api.models import Wallet


class Transaction(Model):
    __tablename__ = 'transaction'

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_update: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())
    type: Mapped[str] = mapped_column(String(30))
    value: Mapped[float] = mapped_column(DECIMAL)
    status: Mapped[str] = mapped_column(String(30))
    sender_id: Mapped[str] = mapped_column(ForeignKey("wallet.id"), nullable=True)
    receiver_id: Mapped[str] = mapped_column(ForeignKey("wallet.id"), nullable=False)
    sender: Mapped["Wallet"] = relationship(back_populates="sender", foreign_keys=[sender_id])
    receiver: Mapped["Wallet"] = relationship(back_populates="receiver", foreign_keys=[receiver_id])
