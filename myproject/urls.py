from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, HttpResponseNotFound
from myapps.views import InfoAPIView, ScriptAPIView, ToolAPIView  # Import necessary views

# Define a simple view for the root URL
def home(request):
    return HttpResponse("Welcome to my Django app!")

# Define the favicon handler
def favicon(request):
    return HttpResponseNotFound()

urlpatterns = [
    path('', home, name='home'),  # Root URL
    path('admin/', admin.site.urls),  # Django admin panel
    path('favicon.ico', favicon),  # Handle favicon.ico requests
    path('api/info/', InfoAPIView.as_view(), name='get_info'),  # Updated to use InfoAPIView
    path('api/get_scripts/<str:stage>/', ScriptAPIView.as_view(), name='get_scripts'),  # API for retrieving scripts
    path('api/get_tools/<str:stage>/', ToolAPIView.as_view(), name='get_tools'),  # API for retrieving tools
]
