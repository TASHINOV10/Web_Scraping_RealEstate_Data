import pandas as pd


apartment_df = pd.read_csv('df_cleaned.csv')
crime_df = pd.read_csv('annual_crime_reports.csv')

average = crime_df['RU9'].mean()

regions = apartment_df['location'].unique()
regions = pd.DataFrame(regions)
regions.to_csv("df_regions.csv", index=False)