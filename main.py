from fastapi import FastAPI
from router.inventory_router import router as inventory_router

app = FastAPI()


app.include_router(
    inventory_router,
    prefix='/api'
)