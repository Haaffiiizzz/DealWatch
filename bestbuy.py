from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

link = "https://www.bestbuy.ca/en-ca/product/dell-inspiron-15-6-laptop-carbon-black-intel-core-i5-1235u-512gb-ssd-16gb-ram-windows-11-home/17862173?source=category&adSlot=1&slotPos=1"
driver.get(link)

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

with open("BestBuyWishlist.json", "w") as file:
    json.dump(wishlist, file)




