from fastapi import APIRouter, Depends, HTTPException, status
from enum import Enum, StrEnum

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.inventory import InventoryORM
from core.schemas import Inventory

router = APIRouter()


class BookingClass(StrEnum):
    First: str = 'First'
    Economy: str = 'Economy'
    Business: str = 'Business'


@router.get(
    '/{flight_number}/{booking_class}',
    response_model=Inventory
)
async def get_information(
    flight_number: str,
    booking_class: BookingClass,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    stmt = (
        select(InventoryORM)
        .where(InventoryORM.flight_number == flight_number)
        .where(InventoryORM.booking_class == booking_class)
    )
    result: Result = await session.execute(stmt)
    inventory_data = result.scalars().one_or_none()
    inventory: Inventory
    if inventory_data is not None:
        inventory: Inventory = Inventory.from_orm(inventory_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Wrong flight_number or booking_class. Please check it!'
        )

    return inventory
