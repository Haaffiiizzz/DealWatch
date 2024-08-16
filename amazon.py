from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from fuzzywuzzy import fuzz


driver = webdriver.Chrome()


link = "https://www.amazon.ca/s?k"
driver.get(link)

def first():
    search = driver.find_element(By.ID, "g")
    search.click()

first()

searchQuery = "32 inch monitor"

def searchSubmit(searchQuery):
    searchBar = driver.find_element(By.ID, "twotabsearchtextbox")
    searchBar.click()
    searchBar.clear()
    searchBar.send_keys(searchQuery)
    searchBar.send_keys(Keys.RETURN)

def getProducts(searchQuery, threshold = 80):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.find_all("div", {"data-component-type" : "s-search-result"})
    
    for item in items:
        titleTag = item.find("div", {"data-cy" : "title-recipe"})
        
        if titleTag:
            title = titleTag.get_text(strip=True)
            score = fuzz.token_set_ratio(searchQuery.lower(), title.lower())
            
            if score >= threshold:
                
                priceWhole = item.find("span", class_ = "a-price-whole")
                priceFraction = item.find("span", class_ = "a-price-fraction")
                
                if priceWhole and priceFraction:
                    price = f"${priceWhole.get_text(strip=True)}{priceFraction.get_text(strip=True)}"
                else:
                    price = None
                    
                print(f"{title}: {price}\n")
        
searchSubmit(searchQuery)
getProducts(searchQuery)





try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    driver.quit()
