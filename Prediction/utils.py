import numpy as np
from geopy.distance import geodesic
from geopy.point import Point


def indexFunction(precipitaion_vec, min_temperature, relative_humidity):
    # Initialize variables
    D = np.zeros_like(precipitaion_vec)
    last_non_zero_index = -1

    # Iterate through the array
    for i in range(len(precipitaion_vec)):
        if precipitaion_vec[i] != 0:
            last_non_zero_index = i
        D[i] = i - last_non_zero_index
    #     D = D+1
    #     print(D-1)
    ####################################
    I = np.zeros_like(precipitaion_vec)
    for day in range(len(min_temperature)):
        if precipitaion_vec[day] == 0:
            idx = 100 + (min_temperature[day] - 10) + 2 * (relative_humidity[day] - 80) / D[day] + precipitaion_vec[day]
            I[day] = idx
        else:
            idx = 100 + (min_temperature[day] - 10) + 2 * (relative_humidity[day] - 80)
            I[day] = idx
    I_total = np.sum(I)
    return I_total


def process_weather_data(data):
    data = np.array(data)
    min_temperature = data[:, 0]  
    relative_humidity = data[:, 1]  
    precipitation = data[:, 2] 

    return round(indexFunction(precipitaion_vec = precipitation, min_temperature=min_temperature, relative_humidity=relative_humidity)/600, 2)



def geodesic_distance(lat1, lon1, lat2, lon2):
    # Create Point objects for the coordinates
    point1 = Point(latitude=lat1, longitude=lon1)
    point2 = Point(latitude=lat2, longitude=lon2)

    # Calculate the geodesic distance using Vincenty formula
    distance = geodesic(point1, point2).kilometers

    return distance