from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationDB(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationGetAllDB(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]
    id: int
    create_date: datetime
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
