import requests
import pandas as pd
from datetime import datetime, timedelta
import glob

class WeatherDataRetriever:
    def __init__(self, input_csv):
        self.input_csv = input_csv
        self.data = pd.read_csv(self.input_csv)
        self.latitudes = self.data['Latitude']
        self.longitudes = self.data['Longitude']
        
    def get_weather_data(self, latitude, longitude):
        url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        parameters = "T2M,PRECTOT,PS,QV2M,RH2M,T2MWET,T2M_MAX,T2M_MIN,T2M_RANGE,TS,WS10M,WS10M_MAX,WS10M_MIN,WS10M_RANGE,WS50M,WS50M_MAX,WS50M_MIN,WS50M_RANGE"
        payload = {
            "parameters": parameters,
            "community": "SB",
            "longitude": longitude,
            "latitude": latitude,
            "start": (datetime.now() - timedelta(days=34)).strftime("%Y%m%d"),
            "end": (datetime.now() - timedelta(days=4)).strftime("%Y%m%d"),
            "format": "CSV"
        }

        response = requests.get(url, params=payload)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch data for Latitude: {latitude}, Longitude: {longitude}")
            return None

    def retrieve_all_weather_data(self):
        for lat, lon in zip(self.latitudes, self.longitudes):
            weather_data = self.get_weather_data(lat, lon)
            if weather_data:
                file_name = f"weather_data_{lat}_{lon}.csv"
                with open(file_name, 'w') as file:
                    file.write(weather_data)
                    print(f"Weather data for Latitude: {lat}, Longitude: {lon} saved to {file_name}")

    def combine_all_weather_data(self):
        file_list = glob.glob('weather_data_*.csv')
        dfs = []

        for file_name in file_list:
            df = pd.read_csv(file_name)
            latitude = float(file_name.split('_')[2])
            longitude = float(file_name.split('_')[3][:-4])
            df['Latitude'] = latitude
            df['Longitude'] = longitude
            dfs.append(df)

        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df.to_csv('combined_weather_data.csv', index=False)
        print("Combined weather data saved to 'combined_weather_data.csv'")