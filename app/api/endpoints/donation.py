from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

# from app.api.validators import (
#     check_charity_project_exists, check_can_delete_project,
#     check_charity_project_opened,
#     check_name_duplicate, check_full_amout_validly)
from app.core.db import get_async_session
from app.crud import donation_crud
from app.schemas import DonationCreate, DonationFull, DonationUser

router = APIRouter()


@router.post(
    '/',
    response_model=DonationUser,
    response_model_exclude_none=True,
)
async def create_donation(
    obj_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(obj_in, session)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationFull],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Возвращает список всех пожертвований."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=DonationUser,
    response_model_exclude_none=True,
)
async def get_user_donations(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    # charity_project = await check_charity_project_exists(project_id, session)
    # await check_can_delete_project(charity_project, session)
    # charity_project = await charity_project_crud.remove(
    #     charity_project, session)
    # return charity_project
    pass
