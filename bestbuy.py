from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

link = "https://www.bestbuy.ca/en-ca/product/logitech-logitech-c922-pro-stream-1080p-hd-webcam-960-001087/10482652?icmp=Recos_5across_yr_rcntly_vwd_home&referrer=Home+Reco_rcntly_vwd"
driver.get(link)

soup = BeautifulSoup(driver.page_source, "html.parser")

print(soup.text.strip())