from sqlalchemy import select  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from app.models import User, Donation
from app.crud.base import CRUDBase
from app.services.donation import donation_in_project


class CRUDDonation(CRUDBase):

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: User
    ):
        obj_in_data = obj_in.dict(exclude_unset=True)

        obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        db_obj = await donation_in_project(session, db_obj)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_user_donations(
            self,
            session: AsyncSession,
            user: User
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
