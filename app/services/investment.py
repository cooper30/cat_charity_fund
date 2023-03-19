from datetime import datetime

from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_not_invested_data(
    session: AsyncSession,
):
    """
    Получение из БД первых по очереди незакрытых проектов и пожертвований.
    """
    project = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested == false()
    ).order_by('create_date'))
    project = project.scalars().first()
    donation = await session.execute(select(Donation).where(
        Donation.fully_invested == false()
    ).order_by('create_date'))
    donation = donation.scalars().first()
    return project, donation


async def investment_process(
    session: AsyncSession,
    obj
):
    """Распределение пожертвований."""
    project, donation = await get_not_invested_data(session)
    if not project or not donation:
        return obj

    close_date = datetime.now()
    balance_project = project.full_amount - project.invested_amount
    balance_donation = donation.full_amount - donation.invested_amount

    if balance_project > balance_donation:
        project.invested_amount += balance_donation
        donation.invested_amount += balance_donation
        donation.fully_invested = True
        donation.close_date = close_date
    elif balance_project == balance_donation:
        project.invested_amount += balance_donation
        donation.invested_amount += balance_donation
        project.fully_invested = True
        donation.fully_invested = True
        project.close_date = close_date
        donation.close_date = close_date
    else:
        project.invested_amount += balance_project
        donation.invested_amount += balance_project
        project.fully_invested = True
        project.close_date = close_date

    session.add(project)
    session.add(donation)
    await session.commit()
    await session.refresh(project)
    await session.refresh(donation)

    return await investment_process(session, obj)
