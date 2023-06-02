from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean  # type: ignore

from app.core.db import Base


class ProjectDonationBaseModel(Base):
    __abstract__ = True
    full_amount = Column(Integer, default=0, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)
