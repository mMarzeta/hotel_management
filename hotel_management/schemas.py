from pydantic import BaseModel
from typing import List
from datetime import datetime


class HotelBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class HotelCreate(HotelBase):
    address_country: str
    address_city: str
    address_post_code: str
    address_street: str
    address_number: int

    class Config:
        orm_mode = True


class Hotel(HotelBase):
    id: int

    class Config:
        orm_mode = True


class RoomBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class RoomCreate(RoomBase):
    hotel_id: int
    size: int

    class Config:
        orm_mode = True


class Room(RoomCreate):
    id: int

    class Config:
        orm_mode = True


class Client(BaseModel):
    client_id: int

    class Config:
        orm_mode = True


class AvailabilityRoomQuery(BaseModel):
    size: int

    class Config:
        orm_mode = True


class AvailabilityRequest(BaseModel):
    date_from: datetime
    date_to: datetime
    rooms: List[AvailabilityRoomQuery]
    allow_room_swaps: bool

    class Config:
        orm_mode = True


class AvailabilityRoomConfiguration(BaseModel):
    date_from = datetime
    date_to = datetime
    room_name = str

    class Config:
        orm_mode = True


class AvailabilityRoomConfigurations(BaseModel):
    configuration: List[AvailabilityRoomConfiguration]
    book_url: str

    class Config:
        orm_mode = True


class AvailabilityConfigurations(BaseModel):
    room: AvailabilityRoomQuery
    configurations: List[AvailabilityRoomConfigurations]

    class Config:
        orm_mode = True


class AvailabilityResponse(BaseModel):
    available: bool
    configurations: List[AvailabilityConfigurations]

    class Config:
        orm_mode = True


class PartialReservationBase(BaseModel):
    date_from: datetime
    date_to: datetime
    room_id: int

    class Config:
        orm_mode = True


class PartialReservationCreate(PartialReservationBase):
    reservation_id: int

    class Config:
        orm_mode = True


class PartialReservation(PartialReservationCreate):
    room_id: int

    class Config:
        orm_mode = True


class ReservationBase(BaseModel):
    client_id: int
    reservation_status: str
    date_from: datetime
    date_to: datetime

    class Config:
        orm_mode = True


class Reservation(ReservationBase):
    partial_reservations: List[PartialReservation]
    reservation_id: int

    class Config:
        orm_mode = True
