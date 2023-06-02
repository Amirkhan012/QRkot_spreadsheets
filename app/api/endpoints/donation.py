from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from app.models import User
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate, DonationDB, DonationGetAllDB)

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(
        donation, session, user=user
    )
    return new_donation


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True,)
async def get_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    user_donations = await donation_crud.get_user_donations(
        session, user=user
    )
    return user_donations


@router.get(
    '/',
    response_model=List[DonationGetAllDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    all_donations = await donation_crud.get_multi(
        session
    )
    return all_donations
