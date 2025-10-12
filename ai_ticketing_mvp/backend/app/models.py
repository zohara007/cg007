# backend/app/models.py
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
import datetime

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True)
    summary = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="Open")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # AI-populated fields
    category = Column(String, index=True)
    priority = Column(String, default="P3") # Default priority for MVP
    assigned_team = Column(String, default="Triage") # Default team for MVP
