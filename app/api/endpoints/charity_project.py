from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from app.api.validators import (
    check_name_duplicate,
    get_charity_project_by_id,
    check_delete,
    check_patch,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate, CharityProjectDB)


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],)
async def create_projects(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(
        charityproject.name, session
    )

    new_charityproject = await charity_project_crud.create(
        charityproject, session
    )
    return new_charityproject


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=List[CharityProjectDB])
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session),
):
    charityprojects = await charity_project_crud.get_multi(session)
    return charityprojects


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],)
async def delete_projects(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_delete(charity_project_id, session)

    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],)
async def update_projects(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):

    charity_project = await get_charity_project_by_id(
        charity_project_id, session
    )

    if obj_in.name:
        await check_name_duplicate(
            obj_in.name, session
        )

    await check_patch(
        obj_in, charity_project, session
    )

    charity_project = await charity_project_crud.update(
        db_obj=charity_project,
        obj_in=obj_in,
        session=session,
    )

    return charity_project
