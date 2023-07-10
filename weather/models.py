from django.db import models

# Create your models here.

class weather_model(models.Model):
    lat = models.DecimalField(max_digits=15, decimal_places=10)
    lon = models.DecimalField(max_digits=15, decimal_places=10)
    detailing_type = models.CharField(max_length=30)
    weather_data = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    