from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


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

# def searchItem(itemName):
#     headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
# }
#     page = requests.get(f"https://www.bestbuy.ca/en-ca/search?search={itemName}", headers=headers)
    
#     soup = BeautifulSoup(page.content, "html.parser")
#     print(soup)
    
# print(searchItem("Samsung Odyssey"))
    
    



