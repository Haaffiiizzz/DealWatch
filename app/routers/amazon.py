from fastapi import APIRouter, Depends, HTTPException
from urllib.parse import unquote
from ..scrapers.amazonScrape import getWishlistData, getDataLink
from ..oauth2 import getCurrentUser
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import TokenData
from .. import models

router = APIRouter(prefix = "/amazon", tags= ["Amazon"]) 

@router.get("/")
def root(currUser: TokenData = Depends(getCurrentUser), db: Session = Depends(get_db)):
    return currUser.id

@router.get("/wishlist")   #change this to post soon
def wishlist(link: str, currUser: TokenData = Depends(getCurrentUser), db: Session = Depends(get_db)):
    # we get link by adding a query to the wishlist path
    link = unquote(link)
    scrapedData = getWishlistData(link)
    
    if not scrapedData:
        raise HTTPException(status_code=404, detail="No data found at the provided link.")

    for item in scrapedData:
        title = item.get("Item")
        brand = item.get("Brand")
        price = item.get("Price")
        imageSrc = item.get("ImageSrc")

        wishlist = models.Amazon(
            userId=currUser.id,
            title=title,
            brand=brand,
            price=price,
            imageSrc=imageSrc
        )

        db.add(wishlist)

    db.commit() 

    return {"message": "Wishlist items added successfully", "items": scrapedData}
    

@router.get("/itemlink")
def itemLink(link: str):
    link = unquote(link)
    return getDataLink(link)

