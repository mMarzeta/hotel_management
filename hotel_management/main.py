from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas, availability_check
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/hotels", response_model=schemas.Hotel)
def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
    return crud.create_hotel(db, hotel)


@app.get("/hotels", response_model=List[schemas.Hotel])
def get_all_hotels(db: Session = Depends(get_db)):
    hotels = crud.get_all_hotels(db)
    return hotels


@app.post("/room", response_model=schemas.Room)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db, room)


@app.get("/room/{hotel_id}", response_model=List[schemas.Room])
def get_rooms_from_hotel(hotel_id: int, db: Session = Depends(get_db)):
    rooms = crud.get_all_rooms_from_hotel(db, hotel_id)
    return rooms


@app.post("/client", response_model=schemas.Client)
def create_mock_client(client: schemas.Client, db: Session = Depends(get_db)):
    return crud.create_client(db, client)


@app.post("/availability", response_model=List[schemas.AvailabilityResponse])
def availability_query(availability: schemas.AvailabilityRequest, db: Session = Depends(get_db)):
    availability_response = availability_check.check_availability(availability, db)
    return availability_response
