from scrapers.amazonScrape import  *
from scrapers.bestbuyScrape import  getSearchData
import time

def compareSearch(searchTerm: str):
    """
    This function will compare the search results of Amazon and BestBuy
    and return data from both. We can then compare the data and see which one is the best match
    and best price for user!
    """
    now = time.time()
    amazonData = getSearchData(searchTerm)
    next = time.time()
    print("Time taken for Amazon: ", next-now)
    
    now = time.time()
    bestBuyData = getSearchData(searchTerm)
    next = time.time()
    print("Time taken for BestBuy: ", next-now)
    
    return amazonData, bestBuyData
now = time.time()
amazon, bestbuy = compareSearch("razer barracuda x")
next = time.time()

print("TIme taken: ", next-now)

print("Amaazon", amazon)
print("BestBuy", bestbuy)