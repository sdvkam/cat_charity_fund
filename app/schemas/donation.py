from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreate(BaseModel):

    full_amount: PositiveInt
    comment: Optional[str]


class DonationUser(DonationCreate):

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationFull(DonationUser):

    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
