from django.urls import path
from .views import *

urlpatterns = [
    path('lateblight/750/data', Prediction, name='fetch_data'),
    path('lateblight/750/all', PredictionAll, name='fetch_data_all'),
]