from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, StrictInt, PositiveInt

from app.core.constants import SchemaConstants as Sc


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=Sc.CHARITY_PROJ_FIELD_MIN_LENGTH,
        max_length=Sc.CHARITY_PROJ_FIELD_MAX_LENGTH,
    )
    description: Optional[str] = Field(
        None, min_length=Sc.CHARITY_PROJ_FIELD_MIN_LENGTH
    )
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=Sc.CHARITY_PROJ_FIELD_MIN_LENGTH,
        max_length=Sc.CHARITY_PROJ_FIELD_MAX_LENGTH,
    )
    description: str = Field(..., min_length=Sc.CHARITY_PROJ_FIELD_MIN_LENGTH)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: StrictInt
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
