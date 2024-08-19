import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

url = 'https://www.amazon.ca/hz/wishlist/ls/1RSXQTAQQ6AQ2?ref_=wl_share'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)


response = requests.get(url, headers=headers)

soup = BeautifulSoup(driver.page_source, 'html.parser')

names = soup.find_all("h2", {"class": "a-size-base"})
prices = soup.find_all("span", {"class": "a-price"})


for name, price in zip(names, prices):

    print(name.text.strip())
    
    whole = price.find("span", {"class": "a-price-whole"})
    frac = price.find("span", {"class": "a-price-fraction"})
    
    print(f"${whole.text.strip()}{frac.text.strip()}\n")
    
print(len(names))