import datetime

from pydantic import BaseModel


class Inventory(BaseModel):
    id: int
    flight_number: str
    booking_class: str
    available_seats: int
    departure_time: datetime.date
    time: datetime.time

    class Config:
        orm_mode = True
        from_attributes = True
