from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def get_charity_project_by_id(
        charityproject_id: int,
        session: AsyncSession,
) -> CharityProject:
    charityproject = await charity_project_crud.get(
        obj_id=charityproject_id, session=session
    )
    if not charityproject:
        raise HTTPException(status_code=404, detail='Проект не найден!')
    return charityproject


async def check_delete(
    charity_project_id: int,
    session: AsyncSession,
):
    charity_project = await get_charity_project_by_id(
        charity_project_id, session=session
    )

    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!")

    return charity_project


async def check_patch(
    obj_in: CharityProjectUpdate,
    charity_project: CharityProject,
    session: AsyncSession,
):
    update_data = obj_in.dict(exclude_unset=True)

    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!")

    if "name" in update_data and update_data["name"] == charity_project.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="При редактировании имя должно быть уникальным.")

    if "full_amount" in update_data and update_data["full_amount"] < charity_project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуемая сумма не может быть меньше уже вложенной.")
