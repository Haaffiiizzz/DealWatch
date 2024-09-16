from fastapi import FastAPI, APIRouter
from .routers import amazon, bestbuy, users
from .models import Base
from .database import engine
from sqlalchemy import MetaData

metadata = MetaData()

Base.metadata.create_all(bind=engine)

app = FastAPI()
router = APIRouter()

@router.get("/")
def root():
    print("Hello sent.")
    return "Hello"

app.include_router(router)
app.include_router(amazon.router)
app.include_router(users.router)
app.include_router(bestbuy.router)
