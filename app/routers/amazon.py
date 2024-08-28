from fastapi import APIRouter
from urllib.parse import unquote
from app.amazonScrape import getWishlistData

router = APIRouter(prefix = "/amazon", tags= ["Amazon"]) 

@router.get("/")
def root():
    print("Amazon sent.")
    return "Amazon"

@router.get("/wishlist/{link:path}")
def wishlist(link: str):
    link = unquote(link)
    trial = 0
    while trial < 5:
        try:
            return getWishlistData(link)
        except Exception as e:
            trial += 1
    return e
        