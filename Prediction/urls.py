from django.urls import path
from .views import *

urlpatterns = [
    path('lateblight/', PredictionView, name='late=blight'),
]