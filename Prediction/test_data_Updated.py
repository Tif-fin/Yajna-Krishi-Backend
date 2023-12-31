from datetime import datetime, timedelta

import torch
import networkx as nx
#import random
import numpy as np
import pandas as pd
#import os
from tqdm import tqdm
import pickle

## Geodesic Distance
from geopy.distance import geodesic
from geopy.point import Point

import torch
from torch_geometric_temporal.signal import StaticGraphTemporalSignal
from torch_geometric_temporal.nn.attention.stgcn import STConv


def laplacian_kernel(distance, sigma):
    return np.exp(-distance / sigma)

'''
def get_stations(filename):
    with open(filename, 'r') as f:
        stations = [line.rstrip('\n') for line in f]
    return stations
'''

def get_features(df, stations):
    target_features = ['QV2M', 'RH2M', 'PRECTOTCORR', 'T2M', 'T2MWET', 'TS', 'PS', 'WS10M', 'WS50M']
    #                    0        1          2           3       4       5     6      7        8
    # Our target labels: [0, 2, 5, 6]

    STATIONS_SNAPSHOTS = []

    # the `pd.Categorical` function is used to convert the 'Location' column to a categorical type with a
    # custom order specified by the `custom_order` list. The `ordered=True` argument ensures that the custom
    # order is respected when performing operations like `groupby`.
    df['Location'] = pd.Categorical(df['Location'], categories=stations, ordered=True)

    grouped_df = df.groupby('Location')

    for _, group in tqdm(grouped_df):
        # Append the features for each station to the list
        snapshot = group[target_features].values.tolist()
        STATIONS_SNAPSHOTS.append(snapshot)

    return STATIONS_SNAPSHOTS


def features_dataframe(df, stations, mean_dict):
    df_new = pd.DataFrame()
    df = df
    selected_features = ['QV2M', 'RH2M', 'PRECTOTCORR', 'T2M', 'T2MWET', 'TS', 'PS', 'WS10M', 'WS50M', 'Location']
    statistics = mean_dict
    for station in stations:
        df_ = df[df['Location'] == station][selected_features]
        # mean = df_.select_dtypes(include=['float']).mean()
        # std = df_.select_dtypes(include=['float']).std()
        mean = statistics[f'{station}_mean']
        std = statistics[f'{station}_std']
        #df_i = df_[selected_features].select_dtypes(include=['float']).apply(lambda x: (x - mean) / std, axis=1)

        # Assuming df_ is your DataFrame and selected_features contains numeric column names
        df_i = (df_[selected_features] - mean) / std
        df_i['Location'] = station

        df_new = pd.concat([df_new, df_i], axis=0, ignore_index=True)

    return df_new

def geodesic_distance(lat1, lon1, lat2, lon2):
    # Create Point objects for the coordinates
    point1 = Point(latitude=lat1, longitude=lon1)
    point2 = Point(latitude=lat2, longitude=lon2)

    # Calculate the geodesic distance using Vincenty formula
    distance = geodesic(point1, point2).kilometers

    return distance


def createWeatherGraph(file_path, desired_ratio):
    """
    It creates the weighted undirected graph based on sensor locations.
    :param file_path: It is the path of csv file which contains the weather attributes together with sensors
    :param desired_ratio: It is the value to control the number of edges so that graph is sufficiently small.
                        Basically it is a percentile on the edge weight. For example, threshold=.033 means
                        only one third of the edges will be considered.
    :return: It gives two outputs edge_index and edge_attr in the form of tensor to be fit in pytorch geometric graph dataset.
    """
    df = pd.read_csv(file_path)
    stations = list(df['Location'].unique())
    latitude = list(df['Latitude'].unique())
    longitude = list(df['Longitude'].unique())
    altitude = list(df['Altitude'].unique())

    # Create an empty graph
    G = nx.Graph()
    for i, station in enumerate(stations):
        alt = df[df['Location'] == station]['Altitude'].iloc[0].item()
        lat = df[df['Location'] == station]['Latitude'].iloc[0].item()
        long = df[df['Location'] == station]['Longitude'].iloc[0].item()
        G.add_node(i, altitude=alt, latitude=lat, longitude=long)

    max_alt_diff = max(altitude) - min(altitude)
    num_nodes = len(stations)
    edge_weights = []
    #geo_distance = []

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            sim =  abs(G.nodes[i]['altitude'] - G.nodes[j]['altitude']) / max_alt_diff
            sim = laplacian_kernel(sim, sigma=0.1)
            g_distance = geodesic_distance(G.nodes[i]['latitude'], G.nodes[i]['longitude'],
                                           G.nodes[j]['latitude'], G.nodes[j]['longitude'])
            # sim = laplacian_kernel(g_distance, sigma=1)

            if g_distance <= 5:
                sim = 1
            edge_weights.append(sim)
            #geo_distance.append(g_distance)
            G.add_edge(i, j)

    edge_weights = torch.tensor(edge_weights)

    #geo_distance = torch.tensor(geo_distance)

    # desired_ratio = 0.35
    threshold = np.percentile(edge_weights, (1 - desired_ratio) * 100)
    mask = edge_weights > threshold
    edge_weights = edge_weights[mask]

    edge_index = torch.tensor(list(G.edges)).t().contiguous()
    edge_index = edge_index[:, mask]

    # Interchange the two rows
    reversed_edge_index = edge_index[[1, 0], :]

    edge_index = torch.cat([edge_index, reversed_edge_index], dim=1)
    edge_weights = torch.tile(edge_weights, (2,))

    self_loop = torch.tile(torch.unique(edge_index[0]), (2,)).reshape(2, len(torch.unique(edge_index[0])))
    edge_index = torch.cat([edge_index, self_loop], dim=1)

    edge_weights = torch.cat([edge_weights, torch.ones(len(self_loop[0]))], dim=0)
    return edge_index, edge_weights, stations



class WeatherTestDatasetLoader(object):

    def __init__(self, snapshots,edge_index,edge_weight):
        self.snapshots = snapshots
        self.edge_index = edge_index
        self.edge_weights = edge_weight
        # Extract the last 500 slices
        # self._snapshots = self._snapshots[-1500:]
        # self._snapshots = np.float32(np.load('C:/Users/megat/Downloads/New folder/snapshots_500.npy'))
##
    def _get_edge_index(self):
        self._edges = self.edge_index#torch.load("./edge_index.pt")
        # self._edges = torch.load("C:/Users/megat/Downloads/New folder/edge_index.pt")
    def _get_edge_weights(self):
        self._edge_weights = self.edge_weights.to(torch.float32)
        # self._edge_weights = torch.load('C:/Users/megat/Downloads/New folder/edge_weights.pt').to(torch.float32)

    def _get_targets_and_features(self):
        stacked_target = self.snapshots
        self.features = [
            np.expand_dims(stacked_target[i: i + self.lags, :], axis=0)
            for i in range(stacked_target.shape[0] - self.lags)
        ]

        self.targets = [
            stacked_target[i + self.lags, :, [0, 2, 5, 6]].T
            for i in range(stacked_target.shape[0] - self.lags)
        ]

    def get_dataset(self, lags: int = 4) -> StaticGraphTemporalSignal:
        self.lags = lags
        self._get_edge_index()
        self._get_edge_weights()
        self._get_targets_and_features()
        dataset = StaticGraphTemporalSignal(
            self._edges, self._edge_weights, self.features, self.targets
        )
        return dataset


def prepareTestData(file_path,end_date,lags,mean_std_file):
    """

    :param file_path:
    :param end_date:
    :param lags:
    :param mean_std_file:
    :return:
    """
    file_path =file_path
    end_date = end_date
    lags =lags
    mean_std_file =mean_std_file
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])

    start_date = end_date - timedelta(days=lags)
    test_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    print(test_df.head())

    desired_edge_ratio = 0.3
    edge_index, edge_weight, stations = createWeatherGraph(file_path=file_path, desired_ratio=desired_edge_ratio)
    
    # Load the Pickle file
    with open(mean_std_file, 'rb') as file:
        mean_dict = pickle.load(file)

    scaled_df_ = features_dataframe(test_df, stations, mean_dict)
    # print(scaled_df_.head())

    # stations_ = get_stations('stations.txt')
    snapshots1 = get_features(scaled_df_, stations)
    snapshots_ = np.transpose(snapshots1, (1, 0, 2))
    # print(snapshots_.shape)
    return snapshots_, edge_index, edge_weight

#Define the neural network structure
class STGCN(torch.nn.Module):
    """
    Processes a sequence of graph data to produce a spatio-temporal embedding
    to be used for regression, classification, clustering, etc.
    prediction time seq. = Lags - 2(Kernel size -1)*STConv_Layers = 41 -2(7-1)*3 = 5 for first STconv and reduded similarly for other
    
    """
    def __init__(self):
        super(STGCN, self).__init__()
        self.stconv_block1 = STConv(210, 14, 32, 64, 9, 3)       # Last is Chebyshev filter size 
        self.stconv_block2 = STConv(210, 64, 128, 256, 7, 3)       # Second last is ouputs 
        self.stconv_block3 = STConv(210, 256, 512, 3, 3, 3)
        #self.fc = torch.nn.Linear(1024, 3)
        
    def forward(self, x, edge_index, edge_attr):
        temp1 = self.stconv_block1(x, edge_index)
        temp2 = self.stconv_block2(temp1, edge_index)
        temp = self.stconv_block3(temp2, edge_index)
        #temp = self.fc(temp3)
        
        return temp

if __name__ == '__main__':
    
    file_path = 'E:/test_df.csv'    #Data from some last recorded dataset 
    end_date = datetime(2023,11,24) #last date
    lags = 15 # last 15 days
    # Specify the file path
    mean_std_file = 'mean_std.pkl'
    
    snapshots,edge_index,edge_weight = prepareTestData(file_path,end_date,lags,mean_std_file)
    print(snapshots.shape)
    
    
    #WeatherTestDatasetLoader
    loader = WeatherTestDatasetLoader(snapshots,edge_index,edge_weight)
    dataset = loader.get_dataset(lags=lags)
    
    '''
    ####
    # Displaying the data in the dataloader
    ####
    # print("=" * 40)
    for data in dataset:
        print(data.y.shape)
        print(data.x.shape)
        print(data.edge_index.shape)
    
        break
    '''
    
    # Define the device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.cuda.empty_cache()
    
    # call the model for inference
    model = STGCN().to(device)
    #print(model)
    
    #cost =0
    for data in dataset:
        y_hat = model(data.x, data.edge_index, data.edge_attr)
        #cost = cost + torch.mean((y_hat - data.y) ** 2)
        print("The value of 10 days forecasting of 3 variables is:", y_hat)
        
    
    
    
