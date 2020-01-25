from sqlalchemy import String, Integer, ForeignKey, Column, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Hotel(Base):
    __tablename__ = "hotel"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    address_country = Column(String)
    address_city = Column(String)
    address_post_code = Column(String)
    address_street = Column(String)
    address_number = Column(String)

    rooms = relationship("Room")


class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey("hotel.id"))
    name = Column(String, unique=True)
    size = Column(Integer)


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer)
    status = Column(String)
    date_from = DateTime(timezone=True)
    date_to = DateTime(timezone=True)

    partial_reservations = relationship("PartialReservation")


class PartialReservation(Base):
    __tablename__ = "partial_reservation"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey("reservation.id"))
    date_from = DateTime(timezone=True)
    date_to = DateTime(timezone=True)
    room_id = Column(Integer)


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer)
