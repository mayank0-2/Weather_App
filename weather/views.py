from django.shortcuts import render
from django.conf import settings
import requests
from weather.models import weather_model
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
# Create your views here.

def home(request): # To render the landing page
    return render(request, 'home.html', {})


def weather(request):   # To handle the submitted location data form the homepage
    if request.method == 'POST':
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        detailing = request.POST['list-radio']
        # print(type(latitude), longitude)
        weather_details = weather_model.objects.filter(lat=latitude, lon=longitude, detailing_type = detailing).first()
        if weather_details :   #if the data is current and available in the database
            print('Database checking...........')
            cutoff_time = timezone.now() - timedelta(minutes= settings.DATA_EXPIRATION_MINUTES)
            print(cutoff_time)
            print(settings.DATA_EXPIRATION_MINUTES)
            print('db time........', weather_details.timestamp)
            print('cutoff time........', cutoff_time.replace(tzinfo=timezone.utc))
            if weather_details.timestamp > cutoff_time.replace(tzinfo=timezone.utc) :
                print('resutl from database')
                return render(request, 'result.html', {'data': weather_details.weather_data})
        
        
        if (detailing == 'Current') : #either current data is old or not available in the database and detailing is current
            print('resutl from api')
            prams = {
                'lat': latitude,
                'lon': longitude,
                'appid': settings.OPENWEATER_API_KEY
            }
            url = "https://api.openweathermap.org/data/2.5/weather?"
            response = requests.get(url, params=prams)
            if response.status_code == 200 :
                weather_model.objects.update_or_create(
                    lat = latitude,
                    lon=longitude,
                    detailing_type=detailing,
                    weather_data= response.json()
                )
                return render(request, 'result.html', {'data':response.json()})
                
        if (detailing == 'Hourly') : #either current data is old or not available and detailiing is 
            prams = {
                'lat': latitude,
                'lon': longitude,
                'appid': settings.OPENWEATER_API_KEY
            }
            url = "https://api.openweathermap.org/data/2.5/forecast?" 
            response = requests.get(url, params=prams)
            if response.status_code == 200 :
                weather_model.objects.update_or_create(
                    lat = latitude,
                    lon=longitude,
                    detailing_type=detailing,
                    weather_data= response.json()
                )
                return render(request, 'result.html', {'data':response.json()})
            
        if (detailing == 'Daily') :
            prams = {
                'lat': latitude,
                'lon': longitude,
                'appid': settings.OPENWEATER_API_KEY
            }
            
            url = "https://api.openweathermap.org/data/2.5/forecast?"
            response = requests.get(url, params=prams)
            print(response)
            if response.status_code == 200 :
                weather_model.objects.update_or_create(
                    lat = latitude,
                    lon=longitude,
                    detailing_type=detailing,
                    weather_data= response.json()
                )
                return render(request, 'result.html', {'data':response.json()})
    return render(request, 'home.html', {})