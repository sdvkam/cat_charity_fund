from datetime import datetime as dt
from sqlalchemy import Boolean, Column, DateTime, Integer, Text, CheckConstraint

from app.core.db import Base


def check_close_donation(context):
    if (
        context.get_current_parameters()['full_amount'] ==
        context.get_current_parameters()['invested_amount']
    ):
        return dt.now()
    return None


class Donation(Base):
    comment = Column(Text)
    full_amount = Column(Integer, CheckConstraint('full_amount>0'))
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=dt.now)
    close_date = Column(DateTime, default=check_close_donation, onupdate=check_close_donation)
