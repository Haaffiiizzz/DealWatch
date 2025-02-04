from ..scrapers.bestbuyScrape import getItemData
from fastapi import APIRouter, HTTPException # Depends,
# from urllib.parse import unquote
# from ..oauth2 import getCurrentUser
# from ..database import get_db
# from sqlalchemy.orm import Session
from ..schemas import LinkData #TokenData, 
# from .. import models

router = APIRouter(prefix = "/bestbuy", tags= ["BestBuy"]) 

@router.get("/")
def root():
    
    return "BestBuy"

@router.get("/itemlink")
def itemLink(link: LinkData): #, currUser: TokenData = Depends(getCurrentUser), db: Session = Depends(get_db)
    
    link = link.url
    scrapedData = getItemData(link)
    
    if not scrapedData:
        raise HTTPException(status_code=404, detail="No data found at the provided link.")

    return scrapedData
    
    

