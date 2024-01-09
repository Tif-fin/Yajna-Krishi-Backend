from django.http import JsonResponse
from .get_weathers import *
from rest_framework.decorators import api_view
from .utils import *
from .models import WeatherPrediction

@api_view(['GET'])
def Prediction(request):
    if request.method == 'GET':
        latitude = request.GET.get('lat')
        longitude = request.GET.get('long')

        if latitude and longitude:
            locations_path = "static/Locations/locations.csv"
            lat_ = [latitude, longitude]

            df_locations = pd.read_csv(locations_path)
            df_locations['Distance'] = df_locations.apply(lambda row: geodesic_distance(*lat_, row['Latitude'], row['Longitude']), axis=1)
        
            min_distance_index = df_locations['Distance'].idxmin()
            location = df_locations.iloc[min_distance_index]

            data_for_current_place = WeatherPrediction.objects.filter(place_name=location['Locations'])
            
            data = {}
            for data_entry in data_for_current_place:
                data['latitude'] = latitude,
                data['longitude'] = longitude,
                data['probability'] = data_entry.lateblight_probability,
                data['predicted_date'] = data_entry.prediction_date
            
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

            data = list(data_for_current_date.values())

            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': Exception}, status=400)
    else:
        return JsonResponse({'error': 'Only GET requests are supported'}, status=405)