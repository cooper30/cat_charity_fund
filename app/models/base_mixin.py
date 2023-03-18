from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer


class TimestampMixin:
    create_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    close_date = Column(DateTime)


class ModelMixin(TimestampMixin):
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, index=True, default=False)
