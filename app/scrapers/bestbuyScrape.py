
from bs4 import BeautifulSoup
import requests
import re

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


def getItemData(itemLink: str):
    
    page = requests.get(itemLink, headers=HEADERS )
        
    soup = BeautifulSoup(page.content, "html.parser")

    nameTag = soup.find("h1", {"class": "font-best-buy text-body-lg font-medium sm:text-title-sm"})
    brandTag = soup.find("a", {"data-automation": "pdp-brandname-link"})
    priceDiv = soup.find("div", {"data-automation": "product-pricing"})
    priceTag = priceDiv.find("span", {"data-automation": "product-price"})
    imageTag = soup.find("img", {"class":"productImage_1NbKv"})
    ratingsTag = soup.find(class_=re.compile(r'^style-module_ratings'))
    numRatingsTag = soup.find("span", {"data-automation": "rating-count"})

    
    Dict = {}
    Dict["Item"] = nameTag.text.strip() if nameTag else None
    Dict["Brand"] = brandTag.text.strip() if brandTag else None
    Dict["Price"] = priceTag.text.strip().split("$")[1] if priceTag else None
    Dict["ImageSrc"] = imageTag.get('src') if imageTag else None
    Dict["rating"] = ratingsTag.text.strip() if ratingsTag else None
    Dict["numRatings"] = numRatingsTag.text.strip("()").split(" ")[0] if numRatingsTag else None

    #returning just a dict of the item

    return Dict

def getSearchData(searchLink: str):
    return True

print(getItemData("https://www.bestbuy.ca/en-ca/product/asus-rog-spatha-x-19000-dpi-wireless-gaming-mouse-black/15952750?icmp=Recos_4across_y_mght_ls_lk"))
    

