from ..scrapers.bestbuyScrape import getItemData
from fastapi import APIRouter, Depends, HTTPException
from urllib.parse import unquote
from ..oauth2 import getCurrentUser
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import TokenData
from .. import models

router = APIRouter(prefix = "/bestbuy", tags= ["BestBuy"]) 

@router.get("/")
def root():
    
    return "BestBuy"

@router.get("/itemlink")
def itemLink(link: str, currUser: TokenData = Depends(getCurrentUser), db: Session = Depends(get_db)):
    # we get link by adding a query to the itemlink path
    link = unquote(link)
    scrapedData = getItemData(link)
    
    if not scrapedData:
        raise HTTPException(status_code=404, detail="No data found at the provided link.")

    for item in scrapedData:
        title = item.get("Item")
        brand = item.get("Brand")
        price = item.get("Price")
        imageSrc = item.get("ImageSrc")

        wishlist = models.BestBuy(
            userId=currUser.id,
            title=title,
            brand=brand,
            price=price,
            imageSrc=imageSrc
        )

        db.add(wishlist)

    db.commit() 

    return {"message": "Wishlist items added successfully", "items": scrapedData}
    # code copied from amazon router. test tomorrow to make sure it works.
    

