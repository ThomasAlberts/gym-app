from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Enum as SAEnum

from backend.src.domain.enums import MovementPattern

class Movement(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str

    movement_pattern: MovementPattern = Field(
        sa_column=SAEnum(MovementPattern, name="movement_pattern_enum")
    )