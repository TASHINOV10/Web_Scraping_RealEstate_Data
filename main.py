
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
tr = {ord(a):ord(b) for a, b in zip(*symbols)}

def scrape_apartment_listings2(url,page_number):

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
    page = []

    listings = soup.find_all('div',class_='listvip-params')
    for listing in listings:

        item_title = listing.find('div', class_='listvip-item-header')
        item_title = item_title.text.strip()

        address = listing.find('div', class_='listvip-item-address')
        address = address.text.strip()
        address = address.split(',')
        address = address[0]

        price = listing.find('span', class_='ads-params-multi first_pclass_vip')
        price = price.text.strip()
        price = price.split()
        try:
            price = ''.join([price[1],price[2],price[3]])
        except:
            price = ''.join([price[1], price[2]])

        rows = listing.find('div', class_='listvip-item-content')
        count = 0
        for row in rows:

            if count == 2: #rooms
                n_rooms = row.text.strip()
                n_rooms = n_rooms.split()
                n_rooms = n_rooms[0]
                n_rooms = list(n_rooms)
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

            if count == 4:
                sqm = row.text.strip()
                sqm = sqm.split()
                sqm = sqm[0]

            if count == 6:
                material = row.text.strip()

            if count == 8:

                row = row.text.strip().split()
                row = row[0]
                year_format = re.compile('^[0-9]{4}')

                if (year_format.match(row)) is not None:
                    year = row

                else:
                    if 'ново' in item_title or 'нова' in item_title or 'нов' in item_title:
                        year = '2023'
                    else:
                        year = 'n/a'

            count += 1


        titles.append(item_title.translate(tr))
        addresses.append(address.translate(tr))
        prices.append(price.translate(tr))
        rooms.append(n_rooms)
        size.append(sqm)
        material_lst.append(material.translate(tr))
        year_lst.append(year)
        page.append(page_number)

    df = pd.DataFrame({
        'location': addresses,
        'title': titles,
        'price_eur': prices,
        'rooms': rooms,
        'm2': size,
        'build_material': material_lst,
        'year': year_lst,
        'page':page_number
    })
    return df




def scrape_apartment_listings(url,page_number):

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
        listings = soup.find_all('div', class_='listtop-item noselect mb20')
        page = []

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

            try:
                price = ''.join([price[0], price[1], price[2]])
            except:
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
                    else:
                        if 'ново' in item_title or 'нова' in item_title or 'нов' in item_title:
                            year = '2023'
                        else:
                            year = 'n/a'

                count += 1

            titles.append(item_title.translate(tr))
            addresses.append(address.translate(tr))
            prices.append(price.translate(tr))
            rooms.append(n_rooms)
            size.append(sqm)
            material_lst.append(material.translate(tr))
            year_lst.append(year)
            page.append(page_number)

        df = pd.DataFrame({
            'location': addresses,
            'title': titles,
            'price_eur': prices,
            'rooms': rooms,
            'm2': size,
            'build_material': material_lst,
            'year': year_lst,
            'page':page
        })


        return df

addresses = []
titles = []
prices = []
rooms = []
size = []
material_lst = []
year_lst =[]
page = []

master_df = pd.DataFrame({
    'location': addresses,
    'title': titles,
    'price_eur': prices,
    'rooms': rooms,
    'm2': size,
    'build_material': material_lst,
    'year': year_lst,
    'page': page
})

url = 'https://www.alo.bg/obiavi/imoti-prodajbi/apartamenti-stai/?region_id=22&location_ids=4342'
df1 = scrape_apartment_listings(url,1)


page_n = 2
page = '&page='
flag = True

while True:
    print(page_n)
    if page_n == 330:
        break

    url2 = f'https://www.alo.bg/obiavi/imoti-prodajbi/apartamenti-stai/?region_id=22&location_ids=4342{page}{page_n}'

    dff1 = scrape_apartment_listings2(url2,page_n)
    dff2 = scrape_apartment_listings2(url2,page_n)
    master_df = [master_df,dff1,dff2]
    master_df = pd.concat(master_df)

    page_n += 1


master_df = [df1,master_df]
master_df = pd.concat(master_df)
print(master_df)



master_df = master_df.drop_duplicates(subset=('title', 'location', 'm2'), keep = 'first')

print(master_df)

#print(master_df['price_eur'])

master_df.to_csv("output.csv", index=False)



