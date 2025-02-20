from playwright.sync_api import sync_playwright

def get_bestbuy_price(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        print(page)

        try:
            price = page.locator('[data-automation="product-pricing"]').inner_text()
            print("Price:", price)
        except:
            print("Price not found.")
        
        browser.close()

# Best Buy Product Page
url = "https://www.bestbuy.ca/en-ca/product/17902796"  # Replace with actual SKU page
get_bestbuy_price(url)
