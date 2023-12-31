from django.http import JsonResponse
from django.conf import settings
from .get_weathers import *


def PredictionView(request):
    if request.method == 'GET':
        documents = {'name':'Prazzwal'}
        return JsonResponse(documents, safe=False)
    return JsonResponse({'message': 'Data received succesfrom rest_framework.decorators import api_viewsfully', 'data': 'Hello'})