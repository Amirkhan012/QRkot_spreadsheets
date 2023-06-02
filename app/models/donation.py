from sqlalchemy import (  # type: ignore
    Column, String, Integer, ForeignKey)

from .base import ProjectDonationBaseModel


class Donation(ProjectDonationBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(String)
