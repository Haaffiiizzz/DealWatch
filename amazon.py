from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()


link = "https://www.amazon.ca/s?k"
driver.get(link)

def first():
    search = driver.find_element(By.ID, "g")
    search.click()

first()

searchQuery = "Gaming PC"

def searchSubmit(searchQuery):
    searchBar = driver.find_element(By.ID, "twotabsearchtextbox")
    searchBar.click()
    searchBar.clear()
    searchBar.send_keys(searchQuery)
    searchBar.send_keys(Keys.RETURN)

def getProducts():
    print("hello")
    

searchSubmit(searchQuery)


soup = BeautifulSoup(driver.page_source, 'html.parser')
items = soup.find_all("div", {"data-component-type" : "s-search-result"})

for item in items:
    name = item.find("h2")
    price = item.find("span", {"class" :"a-price-whole"})
    
    print("\n", "item", name.text, "price", price.text if price else "None", "\n")


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    driver.quit()
