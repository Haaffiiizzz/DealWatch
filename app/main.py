from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.main2 import generateSearchTerm, getAmazonSearch, getBestBuySearch, userPromptSimilarity
from app.schemas import SearchData, Wishlist, WishlistItem
from app.scrapers import amazonScrape
import time


app = FastAPI()
router = APIRouter()

origins = [
   "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@router.get("/")
def root():
    return "Hello"

@router.get("/searchterm")
def compareSearchTerm(body: SearchData):
    """Taking input through the body of the request, this function will generate a search term
    using the user's search input and description. It will then use this search term to get the search results
    from Amazon and BestBuy. It will then compare the search results to the user's description and return the best match.
    We can then return all of this data to the user.
    """
    
    data = {}
    data["input"] = body
    
    userSearch = body.userSearch
    description = body.description
    searchTerm = generateSearchTerm(userSearch, description)
    
    
    amazon, bestbuy = getAmazonSearch(searchTerm), getBestBuySearch(searchTerm)
    
    
    retries = 3
    
    if not amazon:
        trials = 0
        while trials < retries:
            searchTerm = generateSearchTerm(userSearch, description, searchTerm)
            amazon = getAmazonSearch(searchTerm)
            trials += 1

    if not bestbuy:
        trials = 0
        while trials < retries:
            searchTerm = generateSearchTerm(userSearch, description, searchTerm)
            bestbuy = getBestBuySearch(searchTerm)
            trials += 1

    data["Amazon"] = amazon
    data["BestBuy"] = bestbuy
    data["generatedSearchTerm"] = searchTerm
    
    similarityRanking = userPromptSimilarity(amazon, bestbuy, description, userSearch)
    data["ranking"] = similarityRanking
    
    return data

@router.get("/wishlist/")
def getWishlist(body: Wishlist):
    """In this function,  I will first get the items from the amazon wishlist, 
    then I will get search results from Amazon and BestBuy for each item in the wishlist.
    This will be displayed to users so they can see the best price for each item in their wishlist.
    """
    url = body.wishlistURL
    wishListItems = amazonScrape.getWishlistData(url)
    
    return wishListItems

@router.get("/wishlist/search/")
def searchForWishlist(body: WishlistItem):
    """In this function, I will get search results from Amazon and BestBuy for each item in the wishlist.
    Each item is gonna be passed as a json object in the body of the request one at a time.
    This will be displayed to users so they can see the best price for each item in their wishlist.
    """
    item = body.item
    searchTerm = generateSearchTerm(item["Title"]) 
    return searchTerm
    
app.include_router(router)


