
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
tr = {ord(a):ord(b) for a, b in zip(*symbols)}

def scrape_apartment_listings(url):

        page = requests.get(url)
        if page.status_code != 200:
            print("Failed to fetch data from the URL")
            return None

        soup = BeautifulSoup(page.content, 'html.parser')

        titles = []
        addresses = []
        prices = []
        rooms = []
        size = []
        material_lst = []
        year_lst = []
        listings = soup.find_all('div', class_='listtop-item noselect mb20')  # Adjust the class based on the website's HTML structure

        for listing in listings:
            item_title = listing.find('h3', class_='listtop-item-title')
            item_title = item_title.text.strip()
            address = listing.find('div', class_='listtop-item-address')
            address = address.text.strip()
            address = address.split(',')
            address = address[0]

            price = listing.find('span', class_= 'ads-params-single')
            price = price.text.strip()
            price = price.split()
            price = ''.join([price[0], price[1]])

            rows = listing.find_all('div',class_ = 'ads-params-row')
            count = 0
            for row in rows:
                if count == 1:
                    row1 = row.text.strip().split(':')
                    n_rooms = row1[1].split()
                    n_rooms = n_rooms[0]
                    check = list(n_rooms)

                    if check[0] == 'Д':
                        n_rooms = 2
                    elif check[0] == 'Т':
                        n_rooms = 3
                    elif check[0] == 'E':
                        n_rooms = 1
                    elif check[0] == 'М' and check[1] == 'н':
                        n_rooms = 4
                    elif check[0] == 'М' and check[1] == 'е':
                        n_rooms = 10
                    else:
                        n_rooms = 0

                if count == 2:
                    row2 = row.text.strip().split(':')
                    sqm = row2[1].split()
                    sqm = (sqm[0])

                if count == 3:
                    row3 = row.text.strip().split(':')
                    row3 = row3[1].split()
                    material = row3[0]

                if count == 4:
                    row4 = row.text.strip().split(':')
                    row4 = row4[1].split()
                    row4 =row4[0]
                    year_format = re.compile('^[0-9]{4}')
                    if(year_format.match(row4)) is not None:
                        year = row4
                        break
                    else:
                        year = 'n/a'
                        break

                count += 1

            titles.append(item_title.translate(tr))
            addresses.append(address.translate(tr))
            prices.append(price.translate(tr))
            rooms.append(n_rooms)
            size.append(sqm)
            material_lst.append(material.translate(tr))
            year_lst.append(year)

        df = pd.DataFrame({
            'location': addresses,
            'title': titles,
            'price': prices,
            'rooms': rooms,
            'm2': size,
            'build_material': material_lst,
            'year': year_lst
        })

        return df

url = 'https://www.alo.bg/obiavi/imoti-prodajbi/apartamenti-stai/?region_id=22&location_ids=4342'
apartment_data = scrape_apartment_listings(url)

print(apartment_data)

apartment_data.to_csv("output.csv", index=False)