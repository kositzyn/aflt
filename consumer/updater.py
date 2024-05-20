import asyncio
import datetime
import json

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiokafka import AIOKafkaConsumer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class InventoryORM(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_number: Mapped[str]
    booking_class: Mapped[str]
    available_seats: Mapped[int]
    departure_date: Mapped[datetime.date]
    time: Mapped[datetime.time]

    __table_args__ = (
        UniqueConstraint('flight_number', 'booking_class',
                         name='_flight_class_uc'),
    )

async_engine = create_async_engine(
    url='postgresql+asyncpg://user:password@postgres:5432/inventory'
)
async_session = async_sessionmaker(
    bind=async_engine
)


async def updater():
    print(
        f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")} | Updater (Kafka consumer) started...')
    print(
        f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")} | Listening topic "inventory"')

    consumer = AIOKafkaConsumer(
        'inventory',
        bootstrap_servers='kafka:9092'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            data = {}
            try:
                data = json.loads(msg.value.decode())
                print(
                    f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} | Get message {data}')
                print(
                    f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} | Update database...')
                datas = datetime.datetime.fromisoformat(
                    data['departure_date'],
                )
                # Записываем / обновляем БД
                # Если (Номер рейса, класс бронирования) существует - обновляем поле!
                try:
                    async with async_session() as session:
                        stmt = insert(InventoryORM).values(
                            time=datetime.datetime.fromisoformat(
                                data['time'],
                            ),
                            flight_number=data['flight_number'],
                            departure_date=datetime.datetime.fromisoformat(
                                data['departure_date'],
                            ),
                            booking_class=data['booking_class'],
                            available_seats=data['available_seats']
                        ).on_conflict_do_update(
                            index_elements=['flight_number', 'booking_class'],
                            set_=dict(
                                time=datetime.datetime.fromisoformat(
                                    data['time'],
                                ),
                                available_seats=data['available_seats'],
                                departure_date=datetime.datetime.fromisoformat(
                                    data['departure_date'],
                                )
                            )
                        )
                        await session.execute(stmt)
                        await session.commit()
                except Exception as e:
                    print('Database error!!')
                    print(type(e))
                    print(e)

            except json.JSONDecodeError as e:
                print(
                    f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} | Get message')
                print(
                    f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} | Wrong data. It must be json-like')


    finally:
        await consumer.stop()


asyncio.run(updater())
