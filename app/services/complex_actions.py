from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation, User
from app.schemas import CharityProjectCreate, DonationCreate


async def investment_process(
    obj_in: Union[CharityProjectCreate, DonationCreate],
    session: AsyncSession,
    user: Optional[User] = None
):
    data = obj_in.dict()
    if user is not None:
        data['user_id'] = user.id
        model_for_search = CharityProject
        model_for_create = Donation
    else:
        model_for_search = Donation
        model_for_create = CharityProject
    money_need, money_use = data['full_amount'], 0
    objs_with_available_funds = await session.execute(
        select(model_for_search).where(
            model_for_search.fully_invested == 0
        )
    )
    objs_with_available_funds = objs_with_available_funds.scalars().all()
    for obj in objs_with_available_funds:
        money_free = obj.full_amount - obj.invested_amount
        if money_need >= money_free:
            setattr(obj, 'invested_amount', obj.full_amount)
            session.add(obj)
            money_use += money_free
            money_need -= money_free
            if money_need == 0:
                break
        else:
            setattr(obj, 'invested_amount', obj.invested_amount + money_need)
            session.add(obj)
            money_use = data['full_amount']
            break
    data['invested_amount'] = money_use
    db_obj = model_for_create(**data)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj
