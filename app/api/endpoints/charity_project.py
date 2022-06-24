from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_can_delete_project,
                                check_charity_project_exists,
                                check_charity_project_opened,
                                check_full_amout_validly, check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas import (CharityProjectCreate, CharityProjectFull,
                         CharityProjectUpdate)
from app.services.complex_actions import investment_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectFull,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    obj_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Создаёт благотворительный проект."""
    await check_name_duplicate(obj_in.name, session)
    new_charity_project = await investment_process(obj_in, session)
    return new_charity_project


@router.get(
    '/',
    response_model=List[CharityProjectFull],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    all_charity = await charity_project_crud.get_multi(session)
    return all_charity


@router.delete(
    '/{project_id}',
    response_model=CharityProjectFull,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы средства, его можно только закрыть."""
    charity_project = await check_charity_project_exists(project_id, session)
    await check_can_delete_project(charity_project, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session)
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectFull,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Закрытый проект нельзя редактировать; нельзя установить требуемую сумму меньше уже вложенной."""
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_opened(charity_project, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_full_amout_validly(
            charity_project, obj_in.full_amount, session)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project
