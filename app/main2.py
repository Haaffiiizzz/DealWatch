from scrapers import amazonScrape, bestbuyScrape
import time
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
load_dotenv()

#Note: need to fix error handling in getSearches function.
# incase of not finding a search result

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

def generateSearchTerm( userSearch: str, userDescription: str = None, prevGeneratedTerm: str = None):
    """This function will call GPT-4 api to generate a search term based on the user's 
    description and user search input. We can then use this search term to get the search 
    results from Amazon and BestBuy.
    """
    GPT_API_KEY = os.getenv('GPT_API_KEY')
    client = OpenAI(api_key = GPT_API_KEY)
    
    if not prevGeneratedTerm:
        prompt = f"Generate a concise and effective search term for Amazon and Best Buy based on this query: {userSearch}"
        if userDescription:
            prompt += f" and this description: {userDescription}"
        prompt += ". Search term should be as concise as possible."
    else:
        prompt = f"Generate a new search term based on this query: {userSearch}\
        and this description: {userDescription}.You previously generated this \
        search term: {prevGeneratedTerm} It doesn't work, please generate a new\
        search term. Make it more concise and effective."
    
    
        
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
        {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content
    

def userPromptSimilarity(amazonData, bestBuyData):
    """Here I am using gpt to compare the similarity of the search results
    to the user's description and return the best match.
    """
    return True

#


def main():
    description = "I need a good headphones with low latency for gaming. I want it to be wireless and have a good battery life."
    userSearch = "razer headphones"
    searchTerm = generateSearchTerm(userSearch, description)
        
    print(searchTerm)
    amazon, bestbuy = getSearches(searchTerm)
    if not amazon.__class__ == Exception:
        print("Amazon Data:")
        print(amazon)
        for item in amazon:
            print(item)
            print()
        
    
    else:
        print("Couldn't get Amazon Data. Error:", amazon)

    if not bestbuy.__class__ == Exception:
        print("BestBuy Data:")
        print(bestbuy)
        for item in bestbuy:
            print(item)
            print()
        

    else:
        print("Couldn't get BestBuy Data. Error:", bestbuy)
    
    
            
if __name__ == "__main__":
    main()