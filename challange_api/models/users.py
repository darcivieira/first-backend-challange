from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from challange_api.generics.models import Model
from challange_api.models.wallet import Wallet


class Users(Model):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String(150))
    register_number: Mapped[str] = mapped_column(String(18), unique=True)
    email:  Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(30))

    wallet: Mapped["Wallet"] = relationship(back_populates="user")
