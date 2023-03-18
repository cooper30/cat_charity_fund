from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate, check_project_amount,
                                check_project_closed, check_project_exists)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import investment_process

router = APIRouter()


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=List[CharityProjectDB]
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получение списка проектов
    """
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
        body: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Создание проектов
    """
    await check_name_duplicate(body.name, session)
    new_charity_project = await charity_project_crud.create(body, session)
    new_charity_project = await investment_process(
        session,
        new_charity_project
    )
    return new_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Удаление проекта
    """
    project = await check_project_exists(project_id, session)
    check_project_amount(project)
    check_project_closed(project)
    project = await charity_project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    body: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Обновление проекта
    """
    project = await check_project_exists(project_id, session)

    check_project_amount(project, body.full_amount)
    check_project_closed(project)

    if body.name:
        await check_name_duplicate(body.name, session)

    project = await charity_project_crud.update(
        project,
        body,
        session
    )
    return project
