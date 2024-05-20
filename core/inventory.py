import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from core.base import Base

class InventoryORM(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_number: Mapped[str]
    booking_class: Mapped[str]
    available_seats: Mapped[int]
    departure_time: Mapped[datetime.date]
    time: Mapped[datetime.time]

    __table_args__ = (
        UniqueConstraint('flight_number', 'booking_class',
                         name='_flight_class_uc'),
    )