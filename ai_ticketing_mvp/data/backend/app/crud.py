# backend/app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
import uuid

def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).offset(skip).limit(limit).all()

def create_ticket(db: Session, ticket_data: schemas.TicketCreate, predicted_category: str):
    ticket_id = f"PG-2025-{str(uuid.uuid4().int)[:6]}"
    
    db_ticket = models.Ticket(
        ticket_id=ticket_id,
        summary=ticket_data.summary,
        description=ticket_data.description,
        category=predicted_category # Add the AI prediction here
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket