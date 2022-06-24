from sqlalchemy import Column, ForeignKey, Integer, Text, event

from .base import BasicBase, check_fields_full_amount_invested_amount


class Donation(BasicBase):

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)


@event.listens_for(Donation, 'before_update', )
@event.listens_for(Donation, 'before_insert')
def before_create_new_object(mapper, connection, target):
    check_fields_full_amount_invested_amount(target)
