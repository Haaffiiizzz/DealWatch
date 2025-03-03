
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import shutil

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com/',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
}


# options = ChromeOptions()
# options.add_argument("--headless=new")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# DRIVER.get("https://google.com/")


def getItemData(itemLink: str):
    """Here data for a single item is scraped using the items link.
    Requests cant be used here as the data (price specifically) is loaded dynamically using javascript.
    So I am using selenium instead on headless mode.
    """
    # options = ChromeOptions()
    # options.add_argument("--headless=new")
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # DRIVER.get(itemLink)
    
    # soup = BeautifulSoup(DRIVER.page_source, "html.parser")
    
    # DRIVER.quit()
    
    response = requests.get(itemLink, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    
    nameTag = soup.find("h1", {"class": "font-best-buy text-body-lg font-medium sm:text-title-sm"})
    brandTag = soup.find("a", {"data-automation": "pdp-brandname-link"})
    priceDiv = soup.find("div", {"data-automation": "product-pricing"})
    priceTag = priceDiv.find("span", {"data-automation": "product-price"}) if priceDiv else None
    imageTag = soup.find("img", {"class":"productImage_1NbKv"})
    ratingsTag = soup.find(class_=re.compile(r'^style-module_ratings'))
    numRatingsTag = soup.find("span", {"data-automation": "rating-count"})
   
    
    Dict = {}
    Dict["Title"] = nameTag.text.strip() if nameTag else None
    Dict["Brand"] = brandTag.text.strip() if brandTag else None
    Dict["Price"] = priceTag.text.strip().split("$")[1] if priceTag else None
    Dict["ImageSrc"] = imageTag.get('src') if imageTag else None
    Dict["rating"] = ratingsTag.text.strip() if ratingsTag else None
    Dict["numRatings"] = numRatingsTag.text.strip("()").split(" ")[0] if numRatingsTag else None


    return Dict

def getSearchData(searchTerm: str):
    """This function will return a list of dictionaries containing the data of the first 5 items of the search
    and we can look to see which best matches the search term.
    """
    resultsList = []
    searchTerm = searchTerm.replace(" ", "+")
    searchLink = f"https://www.bestbuy.ca/en-ca/search?search={searchTerm}"
    
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    chrome_bin = os.environ.get("GOOGLE_CHROME_BIN") or shutil.which("chrome")
    if not chrome_bin:
        raise Exception("Chrome binary not found!")
    options.binary_location = chrome_bin

    
    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH") or shutil.which("chromedriver")
    if not chromedriver_path:
        raise Exception("Chromedriver not found!")
    service = Service(chromedriver_path)
    
    # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # service = Service(os.environ.get("CHROMEDRIVER_PATH"))
    
    DRIVER = webdriver.Chrome(service=service, options=options)
    
    DRIVER.get(searchLink)
    
    
    try:
        results = WebDriverWait(DRIVER, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Results']"))
        )
    finally:
        soup = BeautifulSoup(DRIVER.page_source, "html.parser")
        DRIVER.quit()
    
    results = soup.find("div", {"aria-label": "Results"})
    if not results:
        raise Exception("No results found")
    items = results.find_all("li")[:5]
    
    for item in items:
        Dict = {}
        
        nameTag = item.find("h3", {"itemprop": "name"})
        priceTag = item.find("span", {"data-automation": "product-price"})
        imageTag = item.find("img")
        ratingTag = item.find("meta", {"itemprop": "ratingValue"})
        numRatingsTag = item.find("meta", {"itemprop": "reviewCount"})
         
        itemLink = item.find("a")
        itemLink = itemLink.get('href') if itemLink else None
        itemLink = f"https://www.bestbuy.ca{itemLink}"
        
        Dict["Title"] = nameTag.text.strip() if nameTag else None
        Dict["Price"] = priceTag.text.strip().split("$")[1] if priceTag else None
        Dict["ImageSrc"] = imageTag.get('src') if imageTag else None
        Dict["rating"] = ratingTag.get('content') if ratingTag else None
        Dict["numRatings"] = numRatingsTag.get('content') if numRatingsTag else None
        Dict["itemLink"] = itemLink
        
        resultsList.append(Dict)
    
    
    
    return resultsList


# print(getItemData("https://www.bestbuy.ca/en-ca/product/17902796"))

# DRIVER.quit()
# print(getSearchData("Razer wireless gaming headphones low latency long battery life"))