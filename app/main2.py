from .scrapers import amazonScrape, bestbuyScrape
import time
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
load_dotenv()

#Note: need to fix error handling in getSearches function.
# incase of not finding a search result

def getAmazonSearch(searchTerm: str):
    """
    This function will get the search results of Amazon and return the data is found 
    else None. We can then compare this with that gotten from BestBuy and see which one is the best match
    and best price for user!
    This takes an average of 1 (one) second.
    """
    try:
        amazonData = amazonScrape.getSearchData(searchTerm)
    except Exception as e:
        print(f"Error fetching Amazon data: {e}")
        amazonData = None
    
    return amazonData

def getBestBuySearch(searchTerm: str):
    """
    This function will get the search results of BestBuy and return the data is found 
    else None. We can then compare this with that gotten from Amazon and see which one is the best match
    and best price for user!
    This takes an average of 13 (thirteen) seconds.
    """
    try:
        bestBuyData = bestbuyScrape.getSearchData(searchTerm)
    except Exception as e:
        print(f"Error fetching BestBuy data: {e}")
        bestBuyData = None

    return bestBuyData

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

    resultString = completion.choices[0].message.content
    resultString = resultString[1:-1]
    return resultString
    

def userPromptSimilarity(amazonData, bestBuyData, userDescription, userSearch):
    """Here I am using gpt to compare the similarity of the search results
    to the user's description and return the best match.
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

    resultString = completion.choices[0].message.content
    resultString = resultString[1:-1]
    return resultString



'''def main():
    description = "I need a good headphones with low latency for gaming. I want it to be wireless and have a good battery life."
    userSearch = "razer headphones"
    searchTerm = generateSearchTerm(userSearch, description)
    print(f"Generated Search Term: {searchTerm}")
        
     
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


    if amazon:
        print("Amazon Data:")
        for item in amazon:
            print(item)
            print()
        
    else:
        print("Couldn't get Amazon Data")

    if bestbuy:
        print("BestBuy Data:")
        for item in bestbuy:
            print(item)
            print()
        
    else:
        print("Couldn't get BestBuy Data")
     
    
            
if __name__ == "__main__":
    main()  '''