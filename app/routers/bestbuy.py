from ..scrapers.bestbuyScrape import getItemData
from fastapi import APIRouter, Depends, HTTPException
from urllib.parse import unquote
from ..oauth2 import getCurrentUser
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import TokenData, LinkData
from .. import models

router = APIRouter(prefix = "/bestbuy", tags= ["BestBuy"]) 

@router.get("/")
def root():
    
    return "BestBuy"

@router.post("/itemlink")
def itemLink(link: LinkData, currUser: TokenData = Depends(getCurrentUser), db: Session = Depends(get_db)):
    
    link = link.url
    scrapedData = getItemData(link)
    
    if not scrapedData:
        raise HTTPException(status_code=404, detail="No data found at the provided link.")


    wishlist = models.BestBuy(
        userId=currUser.id,
        title=scrapedData.get("Item"),
        brand=scrapedData.get("Brand"),
        price=scrapedData.get("Price"),
        imageSrc=scrapedData.get("ImageSrc")
    )

    db.add(wishlist)

    db.commit() 

    return {"message": "Item added successfully", "item": scrapedData}
    
    

