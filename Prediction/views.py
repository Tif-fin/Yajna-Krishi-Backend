from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import WeatherPrediction
from datetime import datetime
from .get_weathers import *
from .utils import *
import pandas as pd

@api_view(['GET'])
def Prediction(request):
    if request.method == 'GET':
        latitude = request.GET.get('lat')
        longitude = request.GET.get('long')

        if latitude and longitude:
            locations_path = "static/Locations/muninipalities.csv"
            lat_ = [latitude, longitude]

            df_locations = pd.read_csv(locations_path)
            df_locations['Distance'] = df_locations.apply(lambda row: geodesic_distance(*lat_, row['Latitude'], row['Longitude']), axis=1)
        
            min_distance_index = df_locations['Distance'].idxmin()
            location = df_locations.iloc[min_distance_index]
            
            nearest_places = df_locations.nsmallest(10, 'Distance')['Location'].tolist()
            
            data_near_place = []
            for place in nearest_places:
                
                data_for_near_place = WeatherPrediction.objects.filter(place_name=place).last()

                data_near = {}

                data_near['id'] = data_for_near_place.id
                data_near['latitude'] = data_for_near_place.latitude
                data_near['longitude'] = data_for_near_place.longitude
                data_near['predicted_weather'] = data_for_near_place.predicted_weather
                data_near['late_blight_probability'] = data_for_near_place.lateblight_probability
                data_near['place_name'] = data_for_near_place.place_name
                data_near['predicted_date'] = data_for_near_place.prediction_date

                data_near_place.append(data_near)

            data_for_current_place = WeatherPrediction.objects.filter(place_name=location['Location']).last()
            
            data = {}
            data['latitude'] = latitude
            data['longitude'] = longitude
            data['probability'] = data_for_current_place.lateblight_probability
            data['predicted_date'] = data_for_current_place.prediction_date
            data['near_places'] = data_near_place
            
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Latitude and longitude parameters are required'}, status=400)
    else:
        return JsonResponse({'error': 'Only GET requests are supported'}, status=405)
    

@api_view(['GET'])
def PredictionAll(request):
    if request.method == 'GET':
        try:
            current_date = datetime.now().date()

            data_for_current_date = WeatherPrediction.objects.filter(prediction_date=current_date)

            # Convert queryset to list of dictionaries
            data = []
            for obj in data_for_current_date:
                data.append({
                    'id': obj.id,
                    'latitude': obj.latitude,
                    'longitude': obj.longitude,
                    'predicted_weather': obj.predicted_weather,
                    'late_blight_probability': obj.lateblight_probability,
                    'place_name': obj.place_name,
                    'predicted_date': obj.prediction_date,
                })

            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only GET requests are supported'}, status=405)
