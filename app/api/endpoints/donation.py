from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud import donation_crud, charity_crud
from app.models import Donation, User
from app.schemas.donation import (
    DonationDBShort,
    DonationDBFull,
    DonationCreate,
)
from app.services.investments import run_investments

router = APIRouter()


@router.get(
    "/",
    response_model=list[DonationDBFull],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Retrieve all existing donations from the database. Available only for
    superusers.
    """
    return await donation_crud.get_all(session)


@router.post(
    "/", response_model=DonationDBShort, response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> Donation:
    """
    Create a new donation. Available only for authenticated users.
    """
    donation = await donation_crud.create(donation, session, user)
    unclosed = await charity_crud.get_unclosed_objects(session)
    if unclosed:
        invested = run_investments(donation, unclosed)
        session.add_all(invested)
    await donation_crud.push_to_db(donation, session)
    return donation


@router.get(
    "/my",
    response_model=list[DonationDBShort],
)
async def get_own_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[Donation]:
    """
    Retrieve your own donations from the database. Available only for
    authenticated users.
    """
    return await donation_crud.get_own_donations(user, session)
