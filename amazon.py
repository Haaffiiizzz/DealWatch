from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()


link = "https://www.amazon.ca/s?k"
driver.get(link)

soup = BeautifulSoup(driver.page_source, 'html.parser')

print(soup)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    driver.quit()
