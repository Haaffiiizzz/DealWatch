from fastapi import APIRouter
from urllib.parse import unquote
from scrapers.bestbuyScrape import getItemData

router = APIRouter(prefix = "/bestbuy", tags= ["BestBuy"]) 

@router.get("/")
def root():
    
    return "BestBuy"

@router.get("/itemlink")
def itemLink(link: str):
    # we get link by adding a query to the itemlink path
    link = unquote(link)
    return getItemData(link)

