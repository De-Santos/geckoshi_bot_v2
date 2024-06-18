import datetime

from sqlalchemy.orm import Mapped, mapped_column

from database.vars import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[int] = mapped_column(default=0)
    createdAt: Mapped[datetime] = mapped_column(default=datetime.datetime.now(datetime.UTC))
