from fastapi import APIRouter, Depends, HTTPException
from urllib.parse import unquote
from ..scrapers.amazonScrape import getWishlistData, getDataLink
from ..oauth2 import getCurrentUser
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import TokenData, LinkData
from .. import models

router = APIRouter(prefix = "/amazon", tags= ["Amazon"]) 

@router.get("/")
def root(currUser: TokenData = Depends(getCurrentUser), db: Session = Depends(get_db)):
    return currUser.id

@router.post("/wishlist")   #change this to post soon
def wishlist(link: LinkData, currUser: TokenData = Depends(getCurrentUser), db: Session = Depends(get_db)):
    # we get link by adding a query to the wishlist path
    link = link.url
    scrapedData = getWishlistData(link)
    
    if not scrapedData:
        raise HTTPException(status_code=404, detail="No data found at the provided link.")

    for item in scrapedData:
        title = item.get("Title")
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
    

@router.post("/itemlink")
def itemLink(link: LinkData, currUser: TokenData = Depends(getCurrentUser), db: Session = Depends(get_db)):
    link = link.url
    scrapedData = getDataLink(link)
    
    if not scrapedData:
        raise HTTPException(status_code=404, detail="No data found at the provided link.")
    
    wishlist = models.Amazon(
            userId=currUser.id,
            title=scrapedData["Title"],
            brand=scrapedData["Brand"],
            price=scrapedData["Price"],
            imageSrc=scrapedData["ImageSrc"]
        )

    db.add(wishlist)

    db.commit() 

    return {"message": "Link item added succesfully", "item": scrapedData}

