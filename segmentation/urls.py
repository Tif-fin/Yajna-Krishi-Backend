from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import late_blight_segmentation
urlpatterns = [
    path("lateblight/",late_blight_segmentation,name='Late Blight Segmentation')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)