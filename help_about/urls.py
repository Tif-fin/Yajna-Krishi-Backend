from django.urls import path
from .views import get_help, about_us

urlpatterns = [
    path('get_help/', get_help, name='get_help'),
    path('about_us/', about_us, name='about_us'),

]