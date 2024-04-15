from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, CheckConstraint

from app.core.base import Base
from app.core.constants import DBConstants as Db


class Investment(Base):
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=Db.INVESTED_AMOUNT_DEFAULT.value)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    __table__args__ = (
        CheckConstraint(
            "full_amount > 0", name=Db.INVESTMENT_CONSTRAINT.value
        ),
        CheckConstraint(
            "invested_amount <= full_amount",
            name=Db.INVESTMENT_LT_FUL_AMOUNT_CONSTRAINT.value,
        ),
        CheckConstraint(
            "invested_amount >= 0", name=Db.INVESTED_AMOUNT_GE_ZERO.value
        )
    )

    def __repr__(self):
        return (f"{type(self).__name__} #{self.id}: "
                f"Current investment amount is: {self.invested_amount}"
                f"/{self.full_amount}. Created at: {self.create_date}, "
                f"closed at: {self.close_date}")
