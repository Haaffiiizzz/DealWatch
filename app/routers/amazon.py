from fastapi import APIRouter
from amazonScrape import getWishlistData

router = APIRouter(prefix = "/amazon", tags= ["Amazon"]) 

@router.get("/")
def root():
    print("Amazon sent.")
    return "Amazon"

@router.get("/wishlist/{link}")
def wishlist(link):
    trial = 0
    while trial < 5:
        try:
            return getWishlistData(link)
        except Exception as e:
            trial += 1
    return e
        