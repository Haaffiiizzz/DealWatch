from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.main2 import generateSearchTerm, getAmazonSearch, getBestBuySearch, userPromptSimilarity
from app.schemas import SearchData, Wishlist, WishlistItem, ItemData, ItemSearch
from app.scrapers import amazonScrape, bestbuyScrape
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
    return {
        "message": "Welcome to the DealWatch API. Check out the documentation at thislink/docs and the code on GitHub at github.com/haaffiiizzz/DealWatch",
        
        "endpoints": {
            "/search/searchterm/": {
                "description": "Search using a search term and description sent through the body of the request",
                "body": {
                    "userSearchTerm": "str",
                    "userDescription": "str"
                }
            },
            "/wishlist/": {
                "description": "Get wishlist data from Amazon through the wishlist URL sent through the body of the request",
                "body": {
                    "wishlistURL": "str"
                }
            },
            "/search/wishlist/": {
                "description": "Search for each item in the wishlist using the returned data from the /wishlist/ endpoint and sent through the body of the request",
                "body": {
                    "item": {
                        "Title": "str"
                    }
                }
            },
            "/item/": {
                "description": "Get data for a particular item using the item link and site sent through the body of the request",
                "body": {
                    "itemLink": "str",
                    "site": "str"
                }
            },
            "/search/item/": {
                "description": "Search for an item using its title using the data returned from the /item/ endpoint and sent through the body of the request",
                "body": {
                    "item": {
                        "Title": "str"
                    }
                }
            }
        }
    }

def getAndCompare(userSearchTerm: str, userDescription: str = None, generatedSearchTerm: str = None):
    '''This function will use the generated search term to get the search results
    from Amazon and BestBuy. It will then compare the search results to the user's description and return the best match.
    We can then return all of this data to the user.'''
    data = {}
    data["input"] = {"userSearch": userSearchTerm, "description": userDescription}
    
    amazon, bestbuy = getAmazonSearch(userSearchTerm), getBestBuySearch(userSearchTerm)

    retries = 3
    
    if not amazon:
        trials = 0
        while trials < retries:
            userSearchTerm = generateSearchTerm(userSearchTerm, userDescription, userSearchTerm)
            amazon = getAmazonSearch(userSearchTerm)
            trials += 1

    if not bestbuy:
        trials = 0
        while trials < retries:
            userSearchTerm = generateSearchTerm(userSearchTerm, userDescription, userSearchTerm)
            bestbuy = getBestBuySearch(userSearchTerm)
            trials += 1

    data["Amazon"] = amazon
    data["BestBuy"] = bestbuy
    data["generatedSearchTerm"] = userSearchTerm
    
    similarityRanking = userPromptSimilarity(amazon, bestbuy, userDescription, userSearchTerm)
    data["ranking"] = similarityRanking
    return data
    
@router.get("/search/searchterm/")
def searchFromSearchTerm(body: SearchData):
    """Taking input through the body of the request, this function will generate a search term
    using the user's search input and description. It will then use these information to call the 
    compareSearchTerm function which will return the search results from Amazon and BestBuy.
    """
    
    userSearchTerm = body.userSearchTerm
    userDescription = body.userDescription
    generatedSearchTerm = generateSearchTerm(userSearchTerm, userDescription)

    try:
        data = getAndCompare(userSearchTerm, userDescription, generatedSearchTerm)
    except Exception as e:
        data = {"error": str(e)}
    return data

@router.get("/wishlist/")
def getWishlist(body: Wishlist):
    """In this function,  I will be returning just the data for wishlist items.
    """
    url = body.wishlistURL
    wishListItems = amazonScrape.getWishlistData(url)
    
    return wishListItems

@router.get("/search/wishlist/")
def searchFromWishlist(body: WishlistItem):
    """In this function, I will get search results from Amazon and BestBuy for each item in the wishlist.
    Each item is gonna be passed as a json object in the body of the request one at a time.
    This will be displayed to users so they can see the best price for each item in their wishlist.
    """
    item = body.item
    searchTerm = generateSearchTerm(item["Title"])
    
    try:
        data = getAndCompare(item["Title"], None, searchTerm)
    except Exception as e:
        data = {"error": str(e)}
    
    return data

@router.get("/item/")
def getItem(body: ItemData):
    """In this function, I will returning just the data for a particular item's link.
    """
    itemLink = body.itemLink
    site = body.site
    
    if site.upper() == "A": #if amazon site
        try:
            item = amazonScrape.getItemData(itemLink)
        except Exception as e:
            item = {"error": str(e)}
    else:
        try:
            item = bestbuyScrape.getItemData(itemLink)
        except Exception as e:
            item = {"error": str(e)}
    
    return item

@router.get("/search/item/")
def searchFromItem(body: ItemSearch):
    """ In this function, I will get search results from Amazon and BestBuy for the item in the body of the request.
    """
    item = body.item
    
    searchTerm = generateSearchTerm(item["Title"])
    try:
        data = getAndCompare(item["Title"], None, searchTerm)
    except Exception as e:
        data = {"error": str(e)}
    
    return data
    
app.include_router(router)


