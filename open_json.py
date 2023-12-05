import geojson
import pandas as pd
from math import radians, cos, sin, sqrt, atan2
def haversine(lat1, lon1, lat2, lon2):
    # Earth radius in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Difference in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance
    distance = R * c
    return distance


#data is translated from cyrillic to latin script
symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
tr = {ord(a):ord(b) for a, b in zip(*symbols)}

region_lst = []
population_lst = []
area_lst = []
coordinates_lst = []
distance_lst = []

with open('population.geojson', encoding='utf-8') as f:
    gj = geojson.load(f)
    features = gj['features']

for feature in features:
    location = feature['geometry']
    coordinates = location.get('coordinates')
    coordinates = coordinates[0][0][0]
    temp= coordinates[1]
    coordinates[1] = coordinates[0]
    coordinates[0] = temp


    properties = feature['properties']
    rajon = properties.get('rajon')
    population = properties.get('nbroi_lica_sum')
    area = properties.get('regname')

    if rajon is not None:
        region_lst.append(rajon.translate(tr))
        area_lst.append(area.translate(tr))
        population_lst.append(population)
        coordinates_lst.append(coordinates)

base_coords = (42.697704, 23.321746)

distance_lst.extend([haversine(base_coords[0], base_coords[1], lat, lon) for lat, lon in coordinates_lst])

demographics = pd.DataFrame(
    {'region': region_lst,
     'area': area_lst,
     'population': population_lst,
     'coordinates': coordinates_lst,
     'distance_from_center': distance_lst
    })
"""
#Removing all rows that contain 0 in population col
index_zero = demographics[demographics['population'] == 0].index
demographics = demographics.drop(index_zero)
demographics.dropna(inplace = True)
"""
demographics.to_csv("population.csv", index=False)
