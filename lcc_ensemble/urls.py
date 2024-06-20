from django.urls import path
from .views import *

urlpatterns = [
    # path('predict_yolo', predict_yolo, name='predict_yolo'),
    # path('predict_mobilenet', predict_mobilenet, name='predict_mobilenet'),
    path('predict', predict, name='predict')
]
