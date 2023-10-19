import pandas as pd

df = pd.read_csv('raw_data.csv')

#Removing all rows that contain false data in build material column
index_material = df[(df['build_material'] != 'Tuhla')
                 & (df['build_material'] != 'Panel')
                 & (df['build_material'] != 'EPK/PK')
                 & (df['build_material'] != 'Gredored')].index

df_filtered = df.drop(index_material)

print(df.shape)
print(df_filtered.shape)

#Removing the "EUR" text and BGN priced apartments from the price eur column
data = df_filtered
new = data["price_eur"].str.split("EUR", n=1, expand=True)
data.drop(columns=["price_eur"], inplace=True)
data["price_eur"] = new[0]

new = data["price_eur"].str.split("lv.", n=1, expand=True)
data.drop(columns=["price_eur"], inplace=True)
data["price_eur"] = new[0]

print(data.shape)

data = data.dropna()
data.to_csv("df_cleaned.csv", index=False)



