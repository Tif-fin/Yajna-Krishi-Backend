from django.urls import path
from .views import *

urlpatterns = [
    path('new', lcc_001, name='lcc_001'),
    path('download', get_download_url, name='get_download_url'),
]