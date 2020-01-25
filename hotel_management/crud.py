from sqlalchemy.orm import Session
from . import models, schemas


def create_hotel(db: Session, hotel: schemas.HotelCreate):
    db_hotel = models.Hotel(name=hotel.name, address_country=hotel.address_country, address_city=hotel.address_city,
                            address_post_code=hotel.address_post_code, address_street=hotel.address_street,
                            address_number=hotel.address_number)
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel


def get_all_hotels(db: Session):
    return db.query(models.Hotel).all()


def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name, hotel_id=room.hotel_id, size=room.size)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def get_all_rooms_from_hotel(db: Session, hotel_id: int):
    return db.query(models.Room).filter(models.Room.hotel_id == hotel_id).all()


def create_client(db: Session, client: schemas.Client):
    db_client = models.Client(client_id=client.client_id)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
