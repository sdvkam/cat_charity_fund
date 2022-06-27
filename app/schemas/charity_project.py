from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, root_validator


class CharityProjectCreate(BaseModel):

    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt

    @root_validator()
    def at_least_fields_query_not_empty_and_null(cls, values):
        print(values)
        for field in values:
            if values[field] in [None, '']:
                raise ValueError(
                    'Название, описание и требуемая сумма для проекта '
                    'должны быть заполнены!'
                )
        return values


class CharityProjectUpdate(BaseModel):

    name: Optional[str] = Field(max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid

    @root_validator()
    def all_fields_query_not_empty_and_null(cls, values):
        errors = 0
        for field in values:
            if values[field] in [None, '']:
                errors += 1
        if errors == 3:
            raise ValueError(
                'Хотябы одно из полей: название, описание, требуемая сумма '
                'должны быть заполнены!'
            )
        return values


class CharityProjectFull(BaseModel):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
