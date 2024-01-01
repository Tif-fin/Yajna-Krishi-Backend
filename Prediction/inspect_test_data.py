import pandas as pd 
import numpy as np 

path = 'static/Test_data/test_data.csv'
location_path = 'static/Locations/locations.csv'

df = pd.read_csv(path)
df_loc = pd.read_csv(location_path)

location1 = set(df_loc['Locations'])

location = set(df["Location"].unique())

# print(location)
print(len(location))
print(len(location1))

print(location - location1)