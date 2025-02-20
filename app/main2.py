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
    
    
    prompt = f"""
You are given two lists of dictionaries containing product data scraped from Amazon and BestBuy. 
Each dictionary has the following structure:
{{
    "Title": "Title of the item",
    "Brand": "Brand of the item",
    "Price": "Price of the item",
    "ImageSrc": "Image URL of the item",
    "numRatings": "Number of ratings the item has",
    "rating": "The rating the item has out of five"
}}

Here is the **Amazon product list**:
{amazonData}

Here is the **BestBuy product list**:
{bestBuyData}

The user is searching for: **"{userSearch}"**
Additional user description: **"{userDescription}"**

### **Task:**
1. **Rank the combined product list** based on:
   - Relevance to the search term and user description.
   - Cheaper price.
   - Higher ratings (if relevance & price are equal).
2. **Return a single list of dictionaries**, ordered from most relevant to least relevant adding one extra key, value which is site as key and name of site as value.
3. **Ensure the top-ranked item is the best fit for the search term & description, while being cost-effective.**
4. **Output JSON format:** A valid JSON list of dictionaries.

Respond with **only the JSON output**, without additional explanation.
"""
    
        
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[ 
        {"role": "user", "content": prompt}
        ]
    )
    result = completion.choices[0].message.content.strip()

    
    if result.startswith("```"):
        result = result.split("```")[1].strip()
        index = result.find("[")
        result = result[index:]
    if result.endswith("```"):
        result = result.split("```")[0].strip()

    try:
        return json.loads(result)
    except json.JSONDecodeError as e:
        print("Error: GPT response is not valid JSON!", e)
        return e
        

