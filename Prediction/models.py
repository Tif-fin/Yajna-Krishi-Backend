from django.db import models
from django.utils import timezone

class WeatherPrediction(models.Model):
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    predicted_weather = models.JSONField()
    lateblight_probability = models.DecimalField(max_digits=5, decimal_places=2)
    place_name = models.CharField(max_length = 100)
    prediction_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Late Blight Prediction for {self.place_name} is  {self.lateblight_probability * 100}% on {self.prediction_date}"
