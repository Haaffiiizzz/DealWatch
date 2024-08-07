import requests
from bs4 import BeautifulSoup
import json

def load_config():
    with open('config.json') as f:
        return json.load(f)

def scrape_data(product):
    config = load_config()
    results = []

    for site in config['websites']:
        url = site['url'].format(product=product)
        response = requests.get(url)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, 'lxml')
        prices = soup.select(site['selectors']['price'])
        prices = [price.get_text().strip() for price in prices]

        results.append({
            'website': site['name'],
            'prices': prices
        })

    return results

if __name__ == "__main__":
    product = "phone"
    results = scrape_data(product)
    print(results)
