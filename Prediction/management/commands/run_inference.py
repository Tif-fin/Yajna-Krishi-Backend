from django.core.management.base import BaseCommand
from geopy.distance import geodesic
from geopy.point import Point
from Prediction.test_data_loader import * 
from Prediction.model import *  
import pandas as pd
import numpy as np
import torch
from Prediction.models import WeatherPrediction
from Prediction.utils import *
from Prediction.get_weathers import process_locations_and_return_csv

class Command(BaseCommand):
    help = 'Run inference'

    def handle(self, *args, **kwargs):
        stations_path = 'static/Stations/stations.txt'
        locations_path = "static/Locations/locations.csv"
        weights_path = 'static/Model_Adam_FT_Last.pth'
        edge_index_path = 'static/Graph/edge_index.pt'
        edge_weight_path = 'static/Graph/edge_weights.pt'
        lags = 43
        pred_seq = 7

        def perform_inference():
            stations = get_stations(stations_path)
            df, Mu_Rho = features_dataframe(process_locations_and_return_csv(locations_path), stations)
        
            snapshot = get_features(df, stations)
            snapshot = np.array(snapshot)
            snap_transpose = np.transpose(snapshot, (1, 0, 2))
        
            edge_index = torch.load(edge_index_path)
            edge_weight = torch.load(edge_weight_path).to(torch.float32)
        
            loader = WeatherDatasetLoader(
                snapshots=snap_transpose,
                edge_index=edge_index,
                edge_weight=edge_weight
            )
            test_dataset = loader.get_dataset(lags=lags, pred_seq=pred_seq)
        
            torch.cuda.empty_cache()
        
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
            model = STGCN().to(device)
            model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
            model.eval()
        
            for data in test_dataset:
                snapshot = data
        
            snapshot = snapshot.to(device)
            y_pred = model(snapshot.x, snapshot.edge_index, snapshot.edge_attr)
        
            station_dict = Mu_Rho
        
            df = pd.DataFrame()
        
            for station, series_obj in station_dict.items():
                data_dict = {'Location': [station]}
                data_dict.update(series_obj.to_dict())
                df = df.append(pd.DataFrame(data_dict), ignore_index=True)
        
            mean = pd.read_csv("static/MeanStd/mean.csv")
            std = pd.read_csv("static/MeanStd/std.csv")
        
            mean_tensor = torch.tensor(mean.iloc[:, 5:8].values, dtype=torch.float32)
            std_tensor = torch.tensor(std.iloc[:, 5:8].values, dtype=torch.float32)
        
            y_pred_ = torch.squeeze(y_pred)
            mean_tensor_broadcasted = np.expand_dims(mean_tensor.detach().numpy(), axis=0)
            std_tensor_broadcasted = np.expand_dims(std_tensor.detach().numpy(), axis=0)
        
            y_pred_denormalized = (y_pred_.detach().numpy() * std_tensor_broadcasted) + mean_tensor_broadcasted
                
            df_locations = pd.read_csv(locations_path)

            try:
                for index, row in df_locations.iterrows():
                    WeatherPrediction.objects.create(
                        longitude=row['Longitude'],
                        latitude=row['Latitude'],
                        place_name = row['Location'],
                        predicted_weather=y_pred_denormalized[:, index].tolist(),
                        lateblight_probability=process_weather_data(y_pred_denormalized[:, index].tolist())
                    )
            except ZeroDivisionError as e:
                print("Error:", e)  

            except Exception as ex:
                # Handle any other exceptions
                print("An error occurred:", ex)  
            finally:
                print("Finally block executed")

        perform_inference()