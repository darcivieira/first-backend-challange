from sqlalchemy import DECIMAL, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from challange_api.generics.models import Model


class Transaction(Model):
    __tablename__ = 'transaction'

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_update: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_onupdate=func.now())
    type: Mapped[str] = mapped_column(String(30))
    value: Mapped[float] = mapped_column(DECIMAL)
    sender_id: Mapped[str] = mapped_column(ForeignKey("wallet.id"), nullable=True)
    sender: Mapped["Wallet"] = relationship(back_populates="transaction_sender", foreign_keys=[sender_id])
    receiver_id: Mapped[str] = mapped_column(ForeignKey("wallet.id"), nullable=False)
    receiver: Mapped["Wallet"] = relationship(back_populates="transaction_receiver", foreign_keys=[receiver_id])
    status: Mapped[str] = mapped_column(String(30))
