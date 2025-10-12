# backend/app/schemas.py
from pydantic import BaseModel
import datetime

# Schema for creating a ticket (what the user sends)
class TicketCreate(BaseModel):
    summary: str
    description: str

# Schema for reading a ticket (what the API returns)
class Ticket(BaseModel):
    id: int
    ticket_id: str
    summary: str
    description: str
    status: str
    created_at: datetime.datetime
    category: str
    priority: str
    assigned_team: str

    class Config:
        orm_mode = True