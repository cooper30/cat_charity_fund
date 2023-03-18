from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, title='Name')
    description: str = Field(..., min_length=1, title='Description')
    full_amount: int = Field(..., gt=0, title='Full Amount')

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):

    @validator('name', 'description')
    def none_and_empty_not_allowed(cls, value: str):
        if not value or value is None:
            raise ValueError('Не заполнены обязательные поля!')
        return value


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        title='Name'
    )
    description: Optional[str] = Field(None, title='Description')
    full_amount: Optional[int] = Field(None, gt=0, title='Full Amount')

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int = Field(..., title='Id')
    invested_amount: int = Field(..., title='Invested Amount')
    fully_invested: bool = Field(..., title='Fully Invested')
    create_date: datetime = Field(..., title='Create Date')
    close_date: Optional[datetime] = Field(None, title='Close Date')

    class Config:
        orm_mode = True
