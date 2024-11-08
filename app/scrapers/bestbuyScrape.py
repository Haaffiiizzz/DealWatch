
from bs4 import BeautifulSoup
import requests
import re


def getItemData(itemLink: str):
    
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}
    page = requests.get(itemLink, headers=headers)
        
    soup = BeautifulSoup(page.content, "html.parser")

    nameTag = soup.find("h1", {"class": "font-best-buy text-body-lg font-medium sm:text-title-sm"})
    brandTag = soup.find("a", {"data-automation": "pdp-brandname-link"})
    priceTag = soup.find("span", {"data-automation": "product-price"})
    imageTag = soup.find("img", {"class":"productImage_1NbKv"})
    ratingsTag = soup.find(class_=re.compile(r'^style-module_ratings'))
    numRatingsTag = soup.find("span", {"data-automation": "rating-count"})

    
    Dict = {}
    Dict["Item"] = nameTag.text.strip() if nameTag else None
    Dict["Brand"] = brandTag.text.strip() if brandTag else None
    Dict["Price"] = priceTag.text.strip().split("$")[1] if priceTag else None
    Dict["ImageSrc"] = imageTag.get('src') if imageTag else None
    Dict["Rating"] = ratingsTag.text.strip() if ratingsTag else None
    Dict["NumRating"] = numRatingsTag.text.strip("()").split(" ")[0] if numRatingsTag else None

    #returning just a dict of the item

    return Dict

