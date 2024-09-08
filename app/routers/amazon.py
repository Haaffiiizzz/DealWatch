from fastapi import APIRouter
from urllib.parse import unquote
from scrapers.amazonScrape import getWishlistData, getDataLink

router = APIRouter(prefix = "/amazon", tags= ["Amazon"]) 

@router.get("/")
def root():
    return "Amazon"

@router.get("/wishlist")
def wishlist(link: str):
    # we get link by adding a query to the wishlist path
    link = unquote(link)
    return getWishlistData(link)

@router.get("/itemlink")
def itemLink(link: str):
    link = unquote(link)
    return getDataLink(link)