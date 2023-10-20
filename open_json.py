import geojson
import pandas as pd


symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
tr = {ord(a):ord(b) for a, b in zip(*symbols)}



region_lst = []
population_lst = []
area_lst = []
with open('population.geojson', encoding='utf-8') as f:
    gj = geojson.load(f)
    featuress = gj['features'][1]
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
demographics.to_csv("test1234.csv", index=False)
print(demographics)

features = gj['features'][173]
print(features)