from fastapi import FastAPI, APIRouter, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from app.main2 import generateSearchTerm, getAmazonSearch, getBestBuySearch, userPromptSimilarity
from app.schemas import SearchData, Wishlist, WishlistItem, ItemData, ItemSearch
from app.scrapers import amazonScrape, bestbuyScrape
import time


app = FastAPI(
    title="DealWatch API",
    description="API for retrieving and comparing deal information from Amazon and BestBuy. "
                "Below you can find detailed documentation for each endpoint along with request and response examples.",
    version="1.0.0"
)

router = APIRouter()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@router.get("/", summary="Welcome Message", description="Returns a welcome message and API documentation links.", tags=["Welcome"])
def root():
    """
    ## Welcome Message
    Returns a welcome message and API documentation links.

    ### Responses:
    - **200**: Welcome message with links to the API docs and GitHub repository.
    """
    
    return {
        "message": "Welcome to the DealWatch API. Check out the documentation at /docs and the code on GitHub at github.com/haaffiiizzz/DealWatch",
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
                "description": "Search for an item using its title with data returned from the /item/ endpoint and sent through the body of the request",
                "body": {
                    "item": {
                        "Title": "str"
                    }
                }
            }
        }
    }

def getAndCompare(userSearchTerm: str, userDescription: str = None, generatedSearchTerm: str = None):
    """
    ## Get and Compare Search Results
    This function uses the provided (or generated) search term to fetch search results from Amazon and BestBuy.
    It then compares these results against the user's description and returns the best match along with all data.

    ### Parameters:
    - **userSearchTerm**: The search term provided by the user.
    - **userDescription**: The description provided by the user (optional).
    - **generatedSearchTerm**: The generated search term (optional).

    ### Returns:
    - **dict**: A dictionary containing:
        - The original input.
        - Search results from Amazon and BestBuy.
        - The final generated search term.
        - A similarity ranking based on the user's description.
    """
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

@router.get(
    "/search/searchterm/", 
    summary="Search Using Search Term", 
    description="Generate a search term using the user's input and description, then return search results from Amazon and BestBuy.",
    tags=["Search Term"], 
    responses={
        200: {
            "description": "Search results from Amazon and BestBuy, including generated search term and ranking",
            "content": {
                "application/json": {
                    "example": {
                        "input": {"userSearch": "razer barracuda x", "description": "gaming headset"},
                        "Amazon": {"result": "Amazon search result example"},
                        "BestBuy": {"result": "BestBuy search result example"},
                        "generatedSearchTerm": "razer gaming headset",
                        "ranking": {"best": "Amazon", "score": 0.95}
                    }
                }
            }
        },
        400: {"description": "Invalid request."},
        500: {"description": "Server error."}
    }
)
def searchFromSearchTerm(body: SearchData = Body(..., example={"userSearchTerm": "razer barracuda x", "userDescription": "gaming headset"})):
    """
    ## Search Using Search Term
    Generate a search term based on the user's search input and description. Returns search results from Amazon and BestBuy.

    ### Request Body:
    - **userSearchTerm**: The search term provided by the user.
    - **userDescription**: The description provided by the user.

    ```json
    {
        "userSearchTerm": "razer barracuda x",
        "userDescription": "gaming headset"
    }
    ```

    ### Responses:
    - **200**: Returns a dictionary containing search results and ranking.
    - **400**: Invalid request.
    - **500**: Server error.
    """
    userSearchTerm = body.userSearchTerm
    userDescription = body.userDescription
    generatedSearchTerm = generateSearchTerm(userSearchTerm, userDescription)

    try:
        data = getAndCompare(userSearchTerm, userDescription, generatedSearchTerm)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return data


@router.get(
    "/wishlist/", 
    summary="Get Wishlist Data", 
    description="Return wishlist items from Amazon using the provided wishlist URL.", 
    tags=["Wishlist"],
    responses={
        200: {
            "description": "Wishlist data retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "wishlistItems": [
                            {"title": "Item 1", "price": "$100"},
                            {"title": "Item 2", "price": "$200"}
                        ]
                    }
                }
            }
        },
        400: {"description": "Invalid request."},
        500: {"description": "Server error."}
    }
)
def getWishlist(body: Wishlist = Body(..., example={"wishlistURL": "https://www.amazon.com/hz/wishlist/ls/EXAMPLE"})):
    """
    ## Get Wishlist Data
    Retrieve data for wishlist items from an Amazon wishlist using the provided URL.

    ### Request Body:
    - **wishlistURL**: The URL of the Amazon wishlist.

    ```json
    {
        "wishlistURL": "https://www.amazon.com/hz/wishlist/ls/EXAMPLE"
    }
    ```

    ### Responses:
    - **200**: Wishlist data.
    - **400**: Invalid request.
    - **500**: Server error.
    """
    url = body.wishlistURL
    wishListItems = amazonScrape.getWishlistData(url)
    return wishListItems

@router.get(
    "/search/wishlist/", 
    summary="Search from Wishlist", 
    description="Perform search queries on each wishlist item using Amazon and BestBuy.", 
    tags=["Wishlist"],
    responses={
        200: {
            "description": "Search results for the wishlist item",
            "content": {
                "application/json": {
                    "example": {
                        "input": {"userSearch": "razer barracuda x", "description": None},
                        "Amazon": {"result": "Amazon wishlist search result"},
                        "BestBuy": {"result": "BestBuy wishlist search result"},
                        "generatedSearchTerm": "razer barracuda x",
                        "ranking": [{"Title": "Razer Barracuda X", "price": 100}]
                    }
                }
            }
        },
        400: {"description": "Invalid request."},
        500: {"description": "Server error."}
    }
)
def searchFromWishlist(body: WishlistItem = Body(..., example={"item": {"Title": "razer barracuda x"}})):
    """
    ## Search from Wishlist
    Use the title of a wishlist item to perform searches on Amazon and BestBuy, returning combined search results.

    ### Request Body:
    - **item**: The wishlist item with a title.

    ```json
    {
        "item": {
            "Title": "razer barracuda x"
        }
    }
    ```

    ### Responses:
    - **200**: Search results for the wishlist item.
    - **400**: Invalid request.
    - **500**: Server error.
    """
    item = body.item
    searchTerm = generateSearchTerm(item["Title"])
    
    try:
        data = getAndCompare(item["Title"], None, searchTerm)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return data

@router.get(
    "/item/", 
    summary="Get Item Data", 
    description="Retrieve detailed data for a specific item using its link and the site identifier.", 
    tags=["Item"],
    responses={
        200: {
            "description": "Item data retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "title": "razer barracuda x",
                        "price": "$150",
                        "specs": {"color": "black", "battery": "10h"}
                    }
                }
            }
        },
        400: {"description": "Invalid site provided."},
        500: {"description": "Server error."}
    }
)
def getItem(body: ItemData = Body(..., example={"itemLink": "https://www.amazon.com/dp/B08FC5L3RG", "site": "A"})):
    """
    ## Get Item Data
    Return detailed data for a specific item from Amazon or BestBuy based on the provided item link and site.

    ### Request Body:
    - **itemLink**: The URL/link to the item.
    - **site**: The identifier for the site ("A" for Amazon, "B" for BestBuy).

    ```json
    {
        "itemLink": "https://www.amazon.com/dp/B08FC5L3RG",
        "site": "A"
    }
    ```

    ### Responses:
    - **200**: Returns the item data.
    - **400**: Invalid site provided.
    - **500**: Server error.
    """
    itemLink = body.itemLink
    site = body.site.upper()

    if site == "A":  # If Amazon
        try:
            item = amazonScrape.getItemData(itemLink)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    elif site == "B":  # If BestBuy
        try:
            item = bestbuyScrape.getItemData(itemLink)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Invalid site. Use 'A' for Amazon or 'B' for BestBuy.")

    return item


@router.get(
    "/search/item/", 
    summary="Search from Item", 
    description="Perform a search using the item title provided in the request body, returning results from Amazon and BestBuy.", 
    tags=["Item"],
    responses={
        200: {
            "description": "Search results for the item.",
            "content": {
                "application/json": {
                    "example": {
                        "input": {"userSearch": "razer barracuda x", "description": None},
                        "Amazon": {"result": "Amazon search result for item"},
                        "BestBuy": {"result": "BestBuy search result for item"},
                        "generatedSearchTerm": "razer barracuda x",
                        "ranking": {}
                    }
                }
            }
        },
        400: {"description": "Invalid request."},
        500: {"description": "Server error."}
    }
)
def searchFromItem(body: ItemSearch = Body(..., example={"item": {"Title": "razer barracuda x"}})):
    """
    ## Search from Item
    Generate search results for an item based on its title. This endpoint uses the title from the provided data to query both Amazon and BestBuy.

    ### Request Body:
    - **item**: The item with its title to be used for the search.

    ```json
    {
        "item": {
            "Title": "razer barracuda x"
        }
    }
    ```

    ### Responses:
    - **200**: Search results for the item.
    - **400**: Invalid request.
    - **500**: Server error.
    """
    item = body.item
    searchTerm = generateSearchTerm(item["Title"])
    try:
        data = getAndCompare(item["Title"], None, searchTerm)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return data
    
app.include_router(router)