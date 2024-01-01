## Geodesic Distance
from geopy.distance import geodesic
from geopy.point import Point


from .test_data_loader import *
from .model import *

test_data_path = 'static/Test_Data/test_data.csv'
stations_path = 'static/Stations/stations.txt'
locations_path = "static/Locations/locations.csv"

# weights_path = './WeatherModel_Weight_100.pth'
weights_path = 'static/WeatherModel_Weight_150.pth'

edge_index_path = 'static/Graph/edge_index.pt'
edge_weight_path = 'static/Graph/edge_weights.pt'

# dataloader parameters
lags = 29
pred_seq = 7

def geodesic_distance(lat1, lon1, lat2, lon2):
    # Create Point objects for the coordinates
    point1 = Point(latitude=lat1, longitude=lon1)
    point2 = Point(latitude=lat2, longitude=lon2)

    # Calculate the geodesic distance using Vincenty formula
    distance = geodesic(point1, point2).kilometers

    return distance

def perform_inference(latitude, longitude):
    stations = get_stations(stations_path)
    df, Mu_Rho = features_dataframe(test_data_path, stations)

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

    lat_ = [latitude, longitude]

    df_locations = pd.read_csv(locations_path)
    df_locations['Distance'] = df_locations.apply(lambda row: geodesic_distance(*lat_, row['Latitude'], row['Longitude']), axis=1)

    min_distance_index = df_locations['Distance'].idxmin()
    min_distance_index2 = df_locations.index.get_loc(min_distance_index)
    
    y_pred_new_location = y_pred_denormalized[:, min_distance_index2, :]
    
    np.set_printoptions(suppress=True, precision=4)
    
    return y_pred_new_location