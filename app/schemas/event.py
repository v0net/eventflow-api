from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class EventBase(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str | None = None
    location: str = Field(min_length=2, max_length=255)
    start_time: datetime
    total_seats: int = Field(gt=0, description="Total seats must be greater than 0")

class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = None
    location: str | None = Field(default=None, min_length=2, max_length=255)
    start_time: datetime | None = None
    total_seats: int | None = Field(default=None, gt=0)


class EventRead(EventBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)