from fastapi import APIRouter, Depends
from urllib.parse import unquote
from ..scrapers.amazonScrape import getWishlistData, getDataLink
from ..oauth2 import getCurrentUser
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import TokenData

router = APIRouter(prefix = "/amazon", tags= ["Amazon"]) 

@router.get("/")
def root(currUser: TokenData = Depends(getCurrentUser), db: Session = Depends(get_db)):
    return currUser.id

@router.get("/wishlist")
def wishlist(link: str):
    # we get link by adding a query to the wishlist path
    link = unquote(link)
    return getWishlistData(link)

@router.get("/itemlink")
def itemLink(link: str):
    link = unquote(link)
    return getDataLink(link)

