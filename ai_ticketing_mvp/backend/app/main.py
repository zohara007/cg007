# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
import joblib
import os

from . import crud, models, schemas
from .database import SessionLocal, engine

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- AI Model Loading ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'nlp', 'saved_models', 'ticket_classifier.joblib')
model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        model = joblib.load(MODEL_PATH)
        print("AI model loaded successfully.")
    except FileNotFoundError:
        print("Model file not found. Please train the model first by running 'nlp/train_model.py'.")
        model = None
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

# --- Dependency for DB Session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ---
@app.post("/api/tickets/", response_model=schemas.Ticket)
def create_new_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    if not model:
        raise HTTPException(status_code=500, detail="AI model is not available.")
    
    # Use the AI model to predict the category
    # The model expects a list of texts, so we pass the description in a list
    predicted_category_array = model.predict([ticket.description])
    predicted_category = predicted_category_array[0] # Get the first (and only) prediction

    print(f"New Ticket Received. Predicted Category: {predicted_category}")
    
    return crud.create_ticket(db=db, ticket_data=ticket, predicted_category=predicted_category)


@app.get("/api/tickets/", response_model=list[schemas.Ticket])
def read_all_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tickets = crud.get_tickets(db, skip=skip, limit=limit)
    return tickets

# --- Static Frontend Serving ---
# Mount the 'static' directory to serve HTML, CSS, JS
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

@app.get("/")
async def read_index():
    # Serve the main index.html file for the root URL
    return FileResponse('backend/static/index.html')