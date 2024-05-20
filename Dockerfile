FROM python:3.11

COPY requirments.txt .

RUN pip install -r requirments.txt

COPY . .

RUN alembic upgrade head

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]