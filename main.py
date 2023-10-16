import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_apartment_listings(url):

    page = requests.get(url)
    if page.status_code != 200:
        print("Failed to fetch data from the URL")
        return None

    soup = BeautifulSoup(page.content, 'html.parser')

    titles = []
    addresses = []
    prices = []

    listings = soup.find_all('div', class_='listtop-item noselect mb20')  # Adjust the class based on the website's HTML structure

    for listing in listings:
        item_title = listing.find('h3', class_='listtop-item-title')
        item_title = item_title.text.strip()
        address = listing.find('div', class_='listtop-item-address')
        address = address.text.strip()
        price = listing.find('span', class_= 'ads-params-single')
        price = price.text.strip()

        n_rooms = soup.find('div', class_= 'ads-params-row')
        print(n_rooms)

        titles.append(item_title)
        addresses.append(address)
        prices.append(price)

    df = pd.DataFrame({
        'Address': addresses,
        'Item Title': titles,
        'Price': prices
    })

    return df


# Example URL of the real estate website
example_url = 'https://www.alo.bg/obiavi/imoti-prodajbi/apartamenti-stai/?region_id=22&location_ids=4342'

# Scrape apartment listings from the example URL
apartment_data = scrape_apartment_listings(example_url)

# Print the DataFrame
print(apartment_data)
