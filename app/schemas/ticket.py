from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TicketCreate(BaseModel):
    event_id: int


class TicketRead(BaseModel):
    id: int
    event_id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)