from sqlalchemy import (  # type: ignore
    Column, String)

from .base import ProjectDonationBaseModel


class CharityProject(ProjectDonationBaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String, nullable=False)
