from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getItemData(itemLink):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options = chrome_options) #options = chrome_options
    
    driver.get(itemLink)
    
    price_tag = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-automation="product-price"]')))
        
    soup = BeautifulSoup(driver.page_source, "html.parser")

    nameTag = soup.find("h1", {"class": "font-best-buy text-body-lg font-medium sm:text-title-sm"})
    brandTag = soup.find("a", {"data-automation": "pdp-brandname-link"})
    priceTag = soup.find("span", {"data-automation": "product-price"})
    imageTag = soup.find("img", {"class":"productImage_1NbKv"})
    

    wishlist = []
    Dict = {}
    Dict["Item"] = nameTag.text.strip() if nameTag else None
    Dict["Brand"] = brandTag.text.strip() if brandTag else None
    Dict["Price"] = priceTag.text.strip().split("$")[1] if priceTag else None
    Dict["ImageSrc"] = imageTag.get('src') if imageTag else None

    wishlist.append(Dict)

    return Dict

# print(getItemData('https://www.bestbuy.ca/en-ca/product/razer-basilisk-v3-26000-dpi-optical-gaming-mouse-black/15688110'))