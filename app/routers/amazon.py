from fastapi import APIRouter, HTTPException
from ..scrapers.amazonScrape import getWishlistData, getDataLink
from ..schemas import LinkData

router = APIRouter(prefix = "/amazon", tags= ["Amazon"]) 

@router.get("/")
def root():
    return "Welcome"

@router.get("/wishlist")
def wishlist(link: LinkData):
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

