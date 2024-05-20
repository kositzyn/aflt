FROM python:3.11

RUN pip install aiokafka
RUN pip install asyncpg
RUN pip install sqlalchemy

COPY . .

CMD ["python", "updater.py"]