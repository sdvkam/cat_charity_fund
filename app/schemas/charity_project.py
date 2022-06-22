from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class CharityProjectCreate(BaseModel):

    name: str = Field(..., max_length=100)
    description: str
    full_amount: int = Field(..., gt=0)

    @validator('full_amount')
    def full_amount_must_more_zero(cls, value: int):
        if value <= 0:
            raise ValueError('Требуемая сумма на проект длжна быть больше нуля.')
        return value


class CharityProjectUpdate(BaseModel):

    name: Optional[str] = Field(max_length=100)
    description: Optional[str]
    full_amount: Optional[int] = Field(gt=0)

    @validator('name')
    def name_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError('Имя для проекта не может быть пустым!')
        return value

    @validator('full_amount')
    def full_amount_cant_be_null(cls, value: int):
        if value is None:
            raise ValueError('Поле для суммы на проект не может быть пустым!')
        return value


class CharityProjectFull(BaseModel):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: int = Field(..., gt=0)
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
