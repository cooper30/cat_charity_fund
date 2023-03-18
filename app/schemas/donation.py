from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class DonationCreate(BaseModel):
    full_amount: int = Field(..., gt=0, title='Full Amount')
    comment: Optional[str] = Field(None, title='Comment')

    class Config:
        extra = Extra.forbid


class DonationDB(DonationCreate):
    id: int = Field(..., title='Id')
    create_date: datetime = Field(..., title='Create Date')

    class Config:
        extra = Extra.forbid
        orm_mode = True


class DonationAdminDB(DonationDB):
    user_id: int = Field(..., title='User Id')
    invested_amount: int = Field(..., title='Invested Amount')
    fully_invested: bool = Field(..., title='Fully Invested')
    close_date: Optional[datetime] = Field(None, title='Close Date')

    class Config:
        extra = Extra.forbid
        orm_mode = True
