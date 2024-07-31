from bs4 import BeautifulSoup

with open("SimpleScraper.html") as file:
    content = file.read()

soup = BeautifulSoup(content, "lxml")
tags = soup.find_all("div")

for div in tags:
    print(div)