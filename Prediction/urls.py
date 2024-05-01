from django.urls import path
from .views import *

urlpatterns = [
    path('lateblight/data', Prediction, name='fetch_data'),
    path('lateblight/all', PredictionAll, name='fetch_data_all'),
]