from django.http import JsonResponse
from django.conf import settings
from .get_weathers import *
from .infer_test import *
from rest_framework.decorators import api_view
from .utils import *

@api_view(['GET'])
def PredictionView(request):
    if request.method == 'GET':
        latitude = request.GET.get('lat')
        longitude = request.GET.get('long')

        if latitude and longitude:
            weather_data = perform_inference(latitude=latitude, longitude=longitude)
            
            data = {
                'probability': process_weather_data(weather_data),
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Latitude and longitude parameters are required'}, status=400)
    else:
        return JsonResponse({'error': 'Only GET requests are supported'}, status=405)