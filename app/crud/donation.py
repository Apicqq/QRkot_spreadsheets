from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate


class CRUDDonation(
    CRUDBase[
        Donation,
        DonationCreate,
        None,
    ]
):
    @staticmethod
    async def get_own_donations(
        user: User, session: AsyncSession
    ) -> list[Donation]:
        """Retrieve list of donations made by user."""
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
