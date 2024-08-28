from amazon import getWishlistData, getDataLink
from bestbuy import getItemData, searchItem
from fastapi import FastAPI
from app.routers import amazon, bestbuy

app = FastAPI()

app.include_router(amazon.router)
app.include_router(bestbuy.router)