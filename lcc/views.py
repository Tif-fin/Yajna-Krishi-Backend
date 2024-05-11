from django.shortcuts import render
import os
# Create your views here.
from rest_framework.decorators import api_view
from django.http import JsonResponse
import mimetypes
from django.http import HttpResponse

# API to check for updates
@api_view(['GET'])
def lcc_001(request):
    # print(request.headers)
    if request.method == 'GET':
        version = request.GET.get('version')
        if version:
            max = [file for file in os.listdir('./lcc/Files/')]
            max.sort()
            latest = max[-1]
            if latest == version:
                return JsonResponse({'status': 'App is up to date', 'latest': latest,'hasUpdate':False})
            elif version not in max:
                return JsonResponse({'error': 'Invalid version'},status=400)
            elif latest != version:
                return JsonResponse({'status': 'Update available', 'latest': latest, 'url':'https://'+request.headers.get('Host')+'/lcc/download?filename='+latest,'hasUpdate':True})
        else:
            return JsonResponse({'error': 'Version parameter is required'}, status=400)
        

# Create download url for latest files
@api_view(['GET'])
def get_download_url(request):
    filename = request.GET.get('filename')
     # fill these variables with real values
    fl_path = 'lcc/Files/' + filename


    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
