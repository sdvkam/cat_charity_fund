from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if not project:
        raise HTTPException(status_code=422, detail='Целевой проект не найден!')
    return project


async def check_charity_project_opened(
    charity_project: CharityProject,
    session: AsyncSession,
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(status_code=422, detail='Целевой проект закрыт!')


async def check_can_delete_project(
    charity_project: CharityProject,
    session: AsyncSession,
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=422,
            detail='Нельзя удалить закрытый проект!'
        )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=422,
            detail=(
                'Нельзя удалить проект, в который уже были '
                'инвестированы средства, его можно только закрыть!'
            )
        )


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession,
) -> None:
    charity_project_id = await charity_project_crud.get_project_id_by_name(
        charity_project_name, session
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Целевой проект с таким именем уже существует!',
        )


async def check_full_amout_validly(
    charity_project: CharityProject,
    new_full_amout: int,
    session: AsyncSession,
) -> None:
    if new_full_amout <= 0 or new_full_amout < charity_project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail=f'Требуемая для проекта сумма должна быть не меньше внесенной суммы = {charity_project.invested_amount}.'
        )
