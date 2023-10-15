import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_apartment_listings(url):

    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch data from the URL")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    titles = []
    addresses = []


    listings = soup.find_all('div', class_='listtop-item noselect mb20')  # Adjust the class based on the website's HTML structure
    for listing in listings:
        item_title = listing.find('h3', class_='listtop-item-title')

        address_element = listing.find('div', class_='c')
        address = address_element.i.get_text(strip=True) if address_element and address_element.i else 'N/A'

        #price = listing.find('div', class_='ads-params-cell  animation-element bounce-up in-view first_pclass').text.strip()
        # Add more data fields as needed

        # Append data to lists
        titles.append(item_title)
        #prices.append(price)
        addresses.append(address)

    # Create a DataFrame
    df = pd.DataFrame({
        'Address': addresses,
        #'Price': prices,
        'Item Title': titles
        # Add more columns as needed
    })

    return df


# Example URL of the real estate website
example_url = 'https://www.alo.bg/obiavi/imoti-prodajbi/apartamenti-stai/?region_id=22&location_ids=4342'

# Scrape apartment listings from the example URL
apartment_data = scrape_apartment_listings(example_url)

# Print the DataFrame
print(apartment_data)
