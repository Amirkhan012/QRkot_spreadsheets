from datetime import datetime

from sqlalchemy import select  # type: ignore

from app.models import Donation


async def project_donation(session, db_obj):
    donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested is not True
        )
    )
    donations = donations.scalars().all()

    if donations:
        right_amount = db_obj.full_amount
        for donation in donations:
            if right_amount <= 0:
                break

            to_add = min(
                donation.full_amount - donation.invested_amount, right_amount)

            if to_add >= right_amount:
                to_add = right_amount

                donation.invested_amount += to_add
                db_obj.invested_amount += to_add
                db_obj.fully_invested = True
                db_obj.close_date = datetime.utcnow()
                right_amount -= to_add

            else:
                donation.invested_amount += to_add
                donation.fully_invested = True
                donation.close_date = datetime.utcnow()
                db_obj.invested_amount += to_add
                right_amount -= to_add

            session.add(donation)
            await session.commit()

    return db_obj
