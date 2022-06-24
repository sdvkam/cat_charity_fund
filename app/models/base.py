from datetime import datetime as dt

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class BasicBase(Base):

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=dt.now)
    close_date = Column(DateTime, default=None)

    __table_args__ = (
        CheckConstraint(
            'full_amount>0 and full_amount>=invested_amount',
            name='check_full_amount'
        ),
    )


def check_fields_full_amount_invested_amount(target):
    if (
        not target.fully_invested and
        target.full_amount == target.invested_amount
    ):
        target.fully_invested = True
        target.close_date = dt.now()
