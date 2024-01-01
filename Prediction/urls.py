from django.urls import path
from .views import *

urlpatterns = [
    path('lateblight/data', PredictionView, name='fetch_data'),
]