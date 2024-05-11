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
from datetime import datetime

class Command(BaseCommand):
    help = 'Run inference'

    def handle(self, *args, **kwargs):
        stations_path = 'static/Stations/stations.txt'
        # locations_path = "static/Locations/locations.csv"
        locations_path = "static/Locations/municipalities.csv"

        weights_path = 'static/Model_60Lags_STConv_Best_Feb18.pt'
        edge_index_path = 'static/Graph/edge_index.pt'
        edge_weight_path = 'static/Graph/edge_weights.pt'
        mean_file_path = "static/MeanStd/mean.csv"
        std_file_path = "static/MeanStd/std.csv"
        test_file_path = "static/Test_Data/test_data.csv" 
        lags = 43
        pred_seq = 24

        def perform_inference():
            latest_data = WeatherPrediction.objects.order_by('prediction_date').first()
            if latest_data:
                print("Latest data is already available")

            else:
                stations = get_stations(stations_path)
                # df, mean_values, std_values = normalizeTestData(process_locations_and_return_csv(locations_path), mean_file_path, std_file_path)
                df, mean_values, std_values = normalizeTestData(test_file_path, mean_file_path, std_file_path)
                snapshot = get_features(df, stations)
                snapshot = np.array(snapshot)
                snap_transpose = np.transpose(snapshot, (1, 0, 2))

                lags_ = snap_transpose.shape[0]

                if lags_ < lags:
                    error_message = (
                        f"Error: Number of lags in test data ({lags_}) is less than "
                        f"the number of lags in the input sequence ({lags}). "
                        "Please make sure that the test data has enough lags to "
                        "cover the input sequence lags. Terminating the program."
                    )
                    raise ValueError(error_message)


                # print(f"snapshots: {snap_transpose.shape}")

                edge_index = torch.load(edge_index_path)#.to(torch.float32)
                edge_weight = torch.load(edge_weight_path).to(torch.float32)

                loader = WeatherDatasetLoader(snapshots=snap_transpose, 
                                                edge_index=edge_index,
                                                edge_weight=edge_weight)
                test_dataset = loader.get_dataset(lags=lags, pred_seq=pred_seq)
                
                torch.cuda.empty_cache()

                # Check if CUDA is available
                device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

                # Move the model to the selected device
                model = STGCN_Best_BRC().to(device)
                # Load the model on CPU if CUDA is not available
                model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
               
                #####################
                ## Evaluation mode on
                #####################
                model.eval()
                
                # Load the data on CPU if CUDA is not available
                for data in test_dataset:
                    snapshot = data
                
                # Move the data to the selected device
                snapshot = snapshot.to(device)
                y_pred = model(snapshot.x, snapshot.edge_index, snapshot.edge_attr)
                print(len(y_pred[0][0][0]))
                #print(y_pred)
              
                ################
                ## de-normalize 
                ################
            
                target_feat = ['T2M_MIN', 'RH2M', 'PRECTOTCORR']
                mean_tensor = torch.tensor(mean_values.iloc[:,[0,1,2,3,4,5,6]].values, dtype=torch.float32)
                std_tensor = torch.tensor(std_values.iloc[:,[0,1,2,3,4,5,6]].values, dtype=torch.float32)
                
                y_pred_ = torch.squeeze(y_pred)
                mean_tensor_broadcasted = np.expand_dims(mean_tensor.detach().numpy(), axis=0)
                std_tensor_broadcasted = np.expand_dims(std_tensor.detach().numpy(), axis=0)

                y_pred_ = y_pred_.cpu().detach().numpy()

                # De-normalize y_pred_
                y_pred_denormalized = (y_pred_ * std_tensor_broadcasted) + mean_tensor_broadcasted

                mask = y_pred_denormalized[:, :, -1]<0
                y_pred_denormalized[mask, -1] = 0
                
                print(y_pred_denormalized.shape)
                df_locations = pd.read_csv(locations_path)

                wart_disease_chance(y_pred_denormalized[:, 1].tolist())
                try:
                    for index, row in df_locations.iterrows():
                        WeatherPrediction.objects.create(
                            longitude=row['longitude'],
                            latitude=row['latitude'],
                            place_name = row['Municipality'],
                            predicted_weather=y_pred_denormalized[:, index].tolist(),
                            wart_probability = wart_disease_chance(y_pred_denormalized[:, index].tolist()),
                            bacterial_wilt_probability = bacterial_wilt_disease_chance(y_pred_denormalized[:, index].tolist()),
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