# """myproject URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path
# from django.http import HttpResponseNotFound

# # Define the favicon handler
# def favicon(request):
#     return HttpResponseNotFound()

# # Merge both URL patterns into one list
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('favicon.ico', favicon),  # Handle favicon.ico requests
#     # other URLs...
# ] 

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from myapps.views import get_info, ScriptAPIView  # Import necessary views

# Define a simple view for the root URL
def home(request):
    return HttpResponse("Welcome to my Django app!")

urlpatterns = [
    path('', home),  # This will serve the root URL ("/")
    path('admin/', admin.site.urls),  # Django admin URL
    path('api/info/', get_info, name='get_info'),  # Path for the 'get_info' API endpoint
    path('api/scripts/', ScriptAPIView.as_view(), name='script_api'),  # Path for your DRF-based Script API view
]

