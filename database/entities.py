import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class BaseInfo:
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    deletedAt = Column(DateTime, default=None)


class User(BaseInfo, Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(type_=BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(type_=BigInteger, unique=True, index=True)
    balance: Mapped[int] = mapped_column(type_=BigInteger, default=0)
    referred_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), type_=BigInteger)
    blocked: Mapped[bool] = mapped_column(default=False)

    referrals: Mapped[List["User"]] = relationship("User", backref="referred_by", remote_side='User.id')
