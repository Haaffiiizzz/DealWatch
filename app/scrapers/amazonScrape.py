#comment

from bs4 import BeautifulSoup
import re
import requests

# url = 'https://www.amazon.ca/hz/wishlist/ls/1RSXQTAQQ6AQ2?ref_=wl_share'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com/',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1'
}

def getWishlistData(wishlistURL: str):
    
 
    site = requests.get(wishlistURL, headers=HEADERS)

    soup = BeautifulSoup(site.content, 'html.parser')

    names = soup.find_all("h2", {"class": "a-size-base"})
    brands = soup.find_all("span", {"class": "a-size-base"})
    prices = soup.find_all("span", {"class": "a-price"})
    images = soup.find_all("img", {"height": "135"})
    ratings = soup.find_all(id=re.compile(r'^review_stars_'))
    numRatings = soup.find_all(id=re.compile(r'^review_count_'))
    

    brands = [brand.text.strip() if brand and "by" in brand.text.strip().lower() else None for brand in brands]   # issue with having tags that fit filter but its not the brand name
    
    wishlist = []

    for nameTag, brand, priceTag, imageSrcTag, rating, numRating in zip(names, brands, prices, images, ratings, numRatings):
        Dict = {}
        
        title = nameTag.text.strip() if nameTag else None
        brand = " ".join(brand.split()[1:])
        
        whole = priceTag.find("span", {"class": "a-price-whole"})
        frac = priceTag.find("span", {"class": "a-price-fraction"})
        price = f"{whole.text.strip()}{frac.text.strip()}" if whole and frac else None
        
        src = imageSrcTag.get('src') if imageSrcTag else None
        numRating = numRating.text.strip() if numRating else None
        rating = rating.text.split(" ")[0]  if rating else None
        
        Dict["Title"] = title
        Dict["Brand"] = brand
        Dict["Price"] = price
        Dict["ImageSrc"] = src
        Dict["numRatings"] = numRating
        Dict["rating"] = rating
    
        wishlist.append(Dict)
    
    return wishlist

def getItemData(itemLink: str):
    Dict = {}

    site = requests.get(itemLink, headers=HEADERS)
    soup = BeautifulSoup(site.content, 'html.parser')
    
    
    titleTag = soup.find("span", {"id": "productTitle"})
    title = titleTag.text.strip() if titleTag else None
    
    wholeTag = soup.find("span", {"class": "a-price-whole"})
    fracTag = soup.find("span", {"class": "a-price-fraction"})
    price = f"{wholeTag.text.strip()}{fracTag.text.strip()}" if wholeTag and fracTag else None
    
    brandTag = soup.find("a", {"id": "bylineInfo"})
    brand = " ".join(brandTag.text.strip().split()[1:]) if brandTag else None
    
    imageTag = soup.find("img", {"id": "landingImage"})
    imageSrc = imageTag.get('src') if imageTag else None
    
    ratingsTag = soup.find("span", {"id": "acrCustomerReviewText"})
    numRatings = ratingsTag.text.split(" ")[0] if ratingsTag else None
    
    ratingTag = soup.find("span", {"id": "acrPopover"})
    rating = ratingTag.text.strip().split()[0] if ratingTag else None
    
    Dict["Title"] = title
    Dict["Brand"] = brand
    Dict["Price"] = price
    Dict["ImageSrc"] = imageSrc
    Dict["numRatings"] = numRatings
    Dict["rating"] = rating
    return Dict

def getSearchData(search: str):
    """This function will return a list of dictionaries containing the data of the first 5 items of the search
    and we can look to see which best matches the search term.
    """
    results = []
    search = search.replace(" ", "+")
    url = f"https://www.amazon.ca/s?k={search}&ref=nb_sb_noss_1"
    
    site = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(site.content, 'html.parser')    
    
    eachItem = soup.find_all("div", {"role": "listitem"})
    top5 = eachItem[4:9]
    
    for item in top5:
        Dict = {}
        titleBrand= item.find("div", {"data-cy": "title-recipe"})
        title = titleBrand.find("h2", {"class":"a-size-base-plus a-spacing-none a-color-base a-text-normal"}).text.strip()
        brand = titleBrand.find("div", {"class": "a-row a-color-secondary"})
        brand = brand.text.strip() if brand else None
        
        reviewsBlock = item.find("div", {"data-cy": "reviews-block"})
        rating = reviewsBlock.find("i", {"data-cy": "reviews-ratings-slot"}).text.strip() if reviewsBlock else None
        rating = rating.split(" ")[0] if rating else None
        numRatings = reviewsBlock.find("span", {"class": "a-size-base s-underline-text"}).text.strip() if reviewsBlock else None
        
        price = item.find("span", {"class": "a-price"})
        price = price.text.strip() if price else None
        price = price.split("$")[1] if price else None
        
        imageSrc = item.find("img", {"class": "s-image"})
        imageSrc = imageSrc.get('src')
        
        itemLink = item.find("a")
        itemLink = itemLink.get('href') if itemLink else None
        itemLink = f"https://www.amazon.ca{itemLink}" if itemLink else None
        
        Dict["Brand"] = brand
        Dict["Title"] = title
        Dict["rating"] = rating
        Dict["numRatings"] = numRatings
        Dict["Price"] = price
        Dict["ImageSrc"] = imageSrc
        Dict["ItemLink"] = itemLink
        
        results.append(Dict)
    
    return results
    
# print(getWishlistData("https://www.amazon.ca/hz/wishlist/ls/1RSXQTAQQ6AQ2?ref_=wl_share")) 
# getSearchData("32 inch 4K gaming monitor 144Hz G-Sync FreeSync HDR low response time")
# for item in getSearchData("razer barracuda x"):
#     print(item, "\n")
#print(getItemData("https://www.amazon.ca/dp/B0BTFNCTXY/?coliid=I2KUWJHA0PQZK2&colid=1RSXQTAQQ6AQ2&psc=0#&ref_=list_c_wl_lv_ov_lig_dp_it"))
