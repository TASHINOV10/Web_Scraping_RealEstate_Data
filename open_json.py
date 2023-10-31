import geojson
import pandas as pd

#data is translated from cyrillic to latin script
symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
tr = {ord(a):ord(b) for a, b in zip(*symbols)}

region_lst = []
population_lst = []
area_lst = []

with open('population.geojson', encoding='utf-8') as f:
    gj = geojson.load(f)
    features = gj['features']

for feature in features:
    properties = feature['properties']
    rajon = properties.get('rajon')
    population = properties.get('nbroi_lica_sum')
    area = properties.get('regname')
    if rajon is not None:
        region_lst.append(rajon.translate(tr))
        area_lst.append(area.translate(tr))
        population_lst.append(population)

demographics = pd.DataFrame(
    {'region': region_lst,
     'area': area_lst,
     'population': population_lst
    })

#Removing all rows that contain 0 in population col
index_zero = demographics[demographics['population'] == 0].index
demographics = demographics.drop(index_zero)
demographics.dropna(inplace = True)

demographics.to_csv("population.csv", index=False)
