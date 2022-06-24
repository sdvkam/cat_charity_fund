from sqlalchemy import CheckConstraint, Column, String, Text, event

from .base import BasicBase, check_fields_full_amount_invested_amount


class CharityProject(BasicBase):

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    __table_args__ = (
        BasicBase.__table_args__[0],
        CheckConstraint('name != ""', name='check_empty_name'),
    )


@event.listens_for(CharityProject, 'before_update')
@event.listens_for(CharityProject, 'before_insert')
def before_create_new_object(mapper, connection, target):
    check_fields_full_amount_invested_amount(target)
