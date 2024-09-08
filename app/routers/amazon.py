from fastapi import APIRouter
from urllib.parse import unquote
from scrapers.amazonScrape import getWishlistData, getDataLink

router = APIRouter(prefix = "/amazon", tags= ["Amazon"]) 

@router.get("/")
def root():
    return "Amazon"

@router.get("/wishlist/{link:path}")
def wishlist(link: str):
    link = unquote(link)
    return getWishlistData(link)

@router.get("/itemlink/{link:path}")
def itemLink(link: str):
    link = unquote(link)
    return getDataLink(link)