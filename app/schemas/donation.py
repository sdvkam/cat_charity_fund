from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class DonationCreate(BaseModel):

    full_amount: int = Field(..., gt=0)
    comment: Optional[str]

    @validator('full_amount')
    def full_amount_must_more_zero(cls, value: int):
        if value <= 0:
            raise ValueError('Сумма пожертвования должна быть больше нуля.')
        return value


class DonationUser(BaseModel):

    full_amount: int = Field(..., gt=0)
    comment: Optional[str]
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationFull(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]
    id: int
    create_date: datetime
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
