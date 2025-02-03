from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, HttpResponseNotFound
from myapps.views import InfoAPIView, ScriptAPIView, ToolAPIView, RegisterUserAPIView, ProjectDetailAPIView

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

    # API Routes
    path('api/info/', InfoAPIView.as_view(), name='get_info'),  # API to retrieve info
    path('api/scripts/<str:stage>/', ScriptAPIView.as_view(), name='get_scripts'),  # API for retrieving scripts by stage
    path('api/tools/<str:stage>/', ToolAPIView.as_view(), name='get_tools'),  # API for retrieving tools by stage
    path('api/register/', RegisterUserAPIView.as_view(), name='user_register'),  # API for user registration
    path('api/projectdetails/', ProjectDetailAPIView.as_view(), name='project_detail_list'),  # API to get all project details
    path('api/projectdetails/<int:pk>/', ProjectDetailAPIView.as_view(), name='project_detail_detail'),  # API for project detail by ID
]
