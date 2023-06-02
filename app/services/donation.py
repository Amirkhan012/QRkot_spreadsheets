from datetime import datetime

from sqlalchemy import select  # type: ignore

from app.models import CharityProject


async def donation_in_project(session, db_obj):
    projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested is not True
        ).order_by(CharityProject.create_date)
    )
    projects = projects.scalars().all()

    if projects:
        total_amount = db_obj.full_amount
        for project in projects:
            if total_amount <= 0:
                break

            to_add = min(total_amount, project.full_amount - project.invested_amount)

            if to_add >= total_amount:
                to_add = total_amount

                project.invested_amount += to_add
                if project.invested_amount == project.full_amount:
                    project.fully_invested = True

                db_obj.invested_amount += to_add
                db_obj.fully_invested = True
                db_obj.close_date = datetime.utcnow()
                total_amount -= to_add

            else:
                project.invested_amount += to_add
                project.fully_invested = True
                project.close_date = datetime.utcnow()
                db_obj.invested_amount += to_add
                total_amount -= to_add

            session.add(project)
            await session.commit()

    return db_obj
