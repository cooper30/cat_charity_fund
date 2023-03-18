from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject

DUPLICATE_NAME_ERR = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND_ERR = 'Проект не найдена!'
PROJECT_CLOSE_ERR = 'Закрытый проект нельзя редактировать!'
PROJECT_RAISING_MONEY_ERR = ('В проект были внесены средства, не подлежит '
                             'удалению!')


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name,
        session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=DUPLICATE_NAME_ERR,
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PROJECT_NOT_FOUND_ERR
        )
    return project


def check_project_closed(project_data):
    if project_data.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_CLOSE_ERR
        )


def check_project_amount(project_data, updated_full_amount=None):
    interest_amount = project_data.invested_amount

    if updated_full_amount:
        if interest_amount > updated_full_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=('Нельзя установить требуемую сумму меньше уже '
                        'вложенной!')
            )
    elif interest_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_RAISING_MONEY_ERR
        )
