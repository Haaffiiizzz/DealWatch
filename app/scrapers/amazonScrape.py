#comment

from bs4 import BeautifulSoup
import re
import requests

# url = 'https://www.amazon.ca/hz/wishlist/ls/1RSXQTAQQ6AQ2?ref_=wl_share'

def getWishlistData(wishlistURL: str):
 
    site = requests.get(wishlistURL)

    soup = BeautifulSoup(site.content, 'html.parser')

    names = soup.find_all("h2", {"class": "a-size-base"})
    brands = soup.find_all("span", {"class": "a-size-base"})
    prices = soup.find_all("span", {"class": "a-price"})
    images = soup.find_all("img", {"height": "135"})
    ratings = soup.find_all(id=re.compile(r'^review_stars_'))
    numRatings = soup.find_all(id=re.compile(r'^review_count_'))
    

    brands = [brand.text.strip() for brand in brands if "by" in brand.text.strip().lower()]   # issue with having tags that fit filter but its not the brand name
    
    wishlist = []

    for nameTag, brand, priceTag, imageSrcTag, rating, numRating in zip(names, brands, prices, images, ratings, numRatings):
        Dict = {}
        
        title = nameTag.text.strip()
        brand = " ".join(brand.split()[1:])
        
        whole = priceTag.find("span", {"class": "a-price-whole"})
        frac = priceTag.find("span", {"class": "a-price-fraction"})
        price = f"{whole.text.strip()}{frac.text.strip()}"
        
        src = imageSrcTag.get('src')
        numRating = numRating.text.strip()
        rating = rating.text.split(" ")[0]
        
        Dict["Title"] = title
        Dict["Brand"] = brand
        Dict["Price"] = price
        Dict["ImageSrc"] = src
        Dict["numRating"] = numRating
        Dict["rating"] = rating
    
        wishlist.append(Dict)
    
    return wishlist

def getDataLink(itemLink: str):
    Dict = {}

    # chrome_options = Options()
    # chrome_options.add_argument("--headless=new")
    # driver = webdriver.Chrome(options = chrome_options)
    # driver.get(itemLink)
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0"
}
    site = requests.get(itemLink, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    
    title = soup.find("span", {"id": "productTitle"}).text.strip()
    
    whole = soup.find("span", {"class": "a-price-whole"}).text.strip()
    frac = soup.find("span", {"class": "a-price-fraction"}).text.strip()
    price = f"{whole}{frac}"
    
    brand = " ".join(soup.find("a", {"id": "bylineInfo"}).text.strip().split()[1:])
    
    image = soup.find("img", {"id": "landingImage"})
    imageSrc = image.get('src')
    
    ratingsTag = soup.find("span", {"id": "acrCustomerReviewText"})

    if ratingsTag:
        
        numRatings = ratingsTag.text # we get something 767 ratings
        numRatings = numRatings.split(" ")[0]
    else:
        numRatings = None
    
    rating = soup.find("span", {"id": "acrPopover"})
    rating = rating.text.strip() if rating else None
    rating = rating.split()[0]
    
    
    Dict["Title"] = title
    Dict["Brand"] = brand
    Dict["Price"] = price
    Dict["ImageSrc"] = imageSrc
    Dict["numRatings"] = numRatings
    Dict["rating"] = rating
    return Dict

# print(getDataLink("https://a.co/d/8XDgttZ"))
print(getWishlistData("https://www.amazon.ca/hz/wishlist/ls/1RSXQTAQQ6AQ2?ref_=wl_share"))