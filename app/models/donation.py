from datetime import datetime as dt
from sqlalchemy import Boolean, Column, event, DateTime, Integer, Text, CheckConstraint

from app.core.db import Base


class Donation(Base):

    comment = Column(Text)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=dt.now)
    close_date = Column(DateTime, default=None)

    __table_args__ = (
        CheckConstraint('full_amount>0 and full_amount>=invested_amount', name='check_full_amount'),
    )


@event.listens_for(Donation, 'before_update')
def user_create_send_password_reset(mapper, connection, target):
    if not target.fully_invested and target.full_amount == target.invested_amount:
        target.fully_invested = True
        target.close_date = dt.now()
