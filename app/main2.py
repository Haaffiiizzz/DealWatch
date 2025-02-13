from scrapers import amazonScrape, bestbuyScrape
import time
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

def getSearches(searchTerm: str):
    """
    This function will compare the search results of Amazon and BestBuy
    and return data from both. We can then compare the data and see which one is the best match
    and best price for user!
    Note: Amazon takes 1 sec, BestBuy takes 13 seconds. Need to optimize BestBuy.
    """
    amazonError = None
    try:
        amazonData = amazonScrape.getSearchData(searchTerm)
    except Exception as e:
        amazonData = None
        amazonError = e

    bestBuyError = None
    try:
        bestBuyData = bestbuyScrape.getSearchData(searchTerm)
    except Exception as e:
        bestBuyData = None
        bestBuyError = e
    
    if amazonError:
        return amazonError, bestBuyData
    elif bestBuyError:
        return amazonData, bestBuyError
    
    return amazonData, bestBuyData

def generateSearchTerm( userSearch: str, userDescription: str = None):
    """This function will generate a search term based on the user's description and search term.
    """
    GPT_API_KEY = os.getenv('GPT_API_KEY')
    client = OpenAI(api_key = GPT_API_KEY)
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
    {"role": "user", "content": "whats a good search term to use on amazon for a gaming keyboard"}
     ]
    )

    print(completion.choices[0].message.content);
    

def userPromptSimilarity(amazonData, bestBuyData):
    """Here I am using gpt text embeddings to compare the similarity of the search results
    to the user's description and return the best match.
    """
    return True
    
'''amazon, bestbuy = getSearches("RAZER BARRACUDA X")
if amazon.__class__ == Exception:
    print("Couldn't get Amazon Data. Error:", amazon)

if bestbuy.__class__ == Exception:
    print("Couldn't get BestBuy Data. Error:", bestbuy)

else:
    
    print("Amazon Data:")
    for item in amazon:
        print(item)
        print()
        
    print("BestBuy Data:")
    for item in bestbuy:
        print(item)
        print()'''
generateSearchTerm("hello")
        
