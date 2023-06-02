from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, validator, Extra, Field


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: PositiveInt

    class Config:
        min_anystr_length = 0


class CharityProjectCreate(CharityProjectBase):
    pass

    @validator('description')
    def validate_description(cls, value):
        if not value:
            raise ValueError("Description cannot be empty")
        return value

    @validator('name')
    def validate_name(cls, value):
        if not value:
            raise ValueError("Name cannot be empty")
        return value


class CharityProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid

    @validator('name')
    def validate_name(cls, name, values):
        if name is None or len(name) > 100 or name.strip() == '':
            raise ValueError("Название проекта не может быть длиннее 100 символов")
        return name

    @validator('description')
    def validate_description(cls, description, values):
        if description is None or description.strip() == '':
            raise ValueError("Описание проекта не может быть пустым")
        return description


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
