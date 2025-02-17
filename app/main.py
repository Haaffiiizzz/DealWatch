from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.main2 import generateSearchTerm, getAmazonSearch, getBestBuySearch


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
def compareSearchTerm(userSearch: str, description: str = None):
    data = {}
    searchTerm = generateSearchTerm(userSearch, description)
    
        
     
    amazon, bestbuy = getAmazonSearch(searchTerm), getBestBuySearch(searchTerm)
    retries = 3
    
    if not amazon:
        trials = 0
        while trials < retries:
            newSearch = generateSearchTerm(userSearch, description, searchTerm)
            amazon = getAmazonSearch(newSearch)
            trials += 1

    if not bestbuy:
        trials = 0
        while trials < retries:
            newSearch = generateSearchTerm(userSearch, description, searchTerm)
            bestbuy = getBestBuySearch(newSearch)
            trials += 1


    
    data["amazon"] = amazon
        
  
    data["bestbuy"] = bestbuy
    
    return data
	

app.include_router(router)


