from fastapi import APIRouter, HTTPException  #Depends, 
from ..scrapers.amazonScrape import getWishlistData, getDataLink
# from ..oauth2 import getCurrentUser
# from ..database import get_db
# from sqlalchemy.orm import Session
from ..schemas import LinkData #TokenData
# from .. import models

router = APIRouter(prefix = "/amazon", tags= ["Amazon"]) 

@router.get("/")
def root():
    return "Welcome"

@router.get("/wishlist")   #change this to post soon
def wishlist(link: LinkData):
    # we get link by adding a query to the wishlist path
    link = link.url
    scrapedData = getWishlistData(link)
    
    if not scrapedData:
        raise HTTPException(status_code=404, detail="No data found at the provided link.")
    return scrapedData
    

@router.get("/itemlink")
def itemLink(link: LinkData):
    link = link.url
    scrapedData = getDataLink(link)
    
    if not scrapedData:
        raise HTTPException(status_code=404, detail="No data found at the provided link.")
    return scrapedData

