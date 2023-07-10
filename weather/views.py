from django.shortcuts import render
import requests
# Create your views here.

def home(request): # To render the landing page
    return render(request, 'home.html', {})


def weather(request):   # To handle the submitted location data form the homepage
    print(request.POST)

    return render(request, 'home.html', {})