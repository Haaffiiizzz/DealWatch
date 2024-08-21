from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

link = "https://www.bestbuy.ca/en-ca/product/logitech-logitech-c922-pro-stream-1080p-hd-webcam-960-001087/10482652?icmp=Recos_5across_yr_rcntly_vwd_home&referrer=Home+Reco_rcntly_vwd"
driver.get(link)

soup = BeautifulSoup(driver.page_source, "html.parser")

nameTag = soup.find("h1", {"class": "font-best-buy text-body-lg font-medium sm:text-title-sm"})
brandTag = soup.find("a", {"data-automation": "pdp-brandname-link"})
priceTag = soup.find("span", {"class": "style-module_screenReaderOnly__4QmbS style-module_large__g5jIz"})


