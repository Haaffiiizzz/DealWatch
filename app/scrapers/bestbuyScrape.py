from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import requests

def getItemData(itemLink):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options = chrome_options)
    
    driver.get(itemLink)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    nameTag = soup.find("h1", {"class": "font-best-buy text-body-lg font-medium sm:text-title-sm"})
    brandTag = soup.find("a", {"data-automation": "pdp-brandname-link"})
    priceTag = soup.find("span", {"data-automation": "product-price"})

    wishlist = []
    Dict = {}
    Dict["Item"] = nameTag.text.strip() if nameTag else None
    Dict["Brand"] = brandTag.text.strip() if brandTag else None
    Dict["Price"] = priceTag.text.strip().split("$")[1] if priceTag else None

    wishlist.append(Dict)

    return Dict

def searchItem(itemName):
    search = requests.get(f"https://www.bestbuy.ca/en-ca/search?search={itemName}")
    
    



