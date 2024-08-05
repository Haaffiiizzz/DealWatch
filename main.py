from bs4 import BeautifulSoup

countryInfo = {}

with open("SimpleScraper.html") as file:
    content = file.read()

soup = BeautifulSoup(content, "lxml")
country_div = soup.find_all("div", class_ = "row")

for div in country_div:
    if div.h3:
        name = div.h3.text.strip()
        info = div.find("div", class_ = "country-info")
        
        if info:
            countryDict = {}
            info = info.text.strip()
            info = info.split("\n")
            
            for data in info:
                data = data.split(": ")
                countryDict[data[0]] = data[1]
            
            countryInfo[name] = countryDict
           

print(countryInfo)