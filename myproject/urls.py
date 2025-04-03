# from django.contrib import admin
# from django.urls import path
# from django.http import HttpResponse, HttpResponseNotFound
# from myapps.views import InfoAPIView, LoginUserAPIView, ScriptAPIView, ToolAPIView, RegisterUserAPIView, ProjectDetailAPIView

# # Define a simple view for the root URL
# def home(request):
#     return HttpResponse("Welcome to my Django app!")

# # Define the favicon handler
# def favicon(request):
#     return HttpResponseNotFound()

# urlpatterns = [
#     path('', home, name='home'),  # Root URL
#     path('admin/', admin.site.urls),  # Django admin panel
#     path('favicon.ico', favicon),  # Handle favicon.ico requests

#     # API Routes
#     path('api/info/', InfoAPIView.as_view(), name='get_info'),  # API to retrieve info
#     path('api/scripts/<str:stage>/', ScriptAPIView.as_view(), name='get_scripts'),  # API for retrieving scripts by stage
#     path('api/tools/<str:stage>/', ToolAPIView.as_view(), name='get_tools'),  # API for retrieving tools by stage
#     path('api/register/', RegisterUserAPIView.as_view(), name='user_register'),  # API for user registration
#     path('api/login/', LoginUserAPIView.as_view(), name='user_login'),  # API for user login
#     path('api/projectdetails/', ProjectDetailAPIView.as_view(), name='project_detail_list'),  # API to get all project details
#     path('api/projectdetails/<int:pk>/', ProjectDetailAPIView.as_view(), name='project_detail_detail'),  # API for project detail by ID
# ]

# from django.contrib import admin
# from django.urls import path, include
# from django.http import HttpResponse
# from django.conf import settings
# from django.conf.urls.static import static
# from django.views.generic import RedirectView

# # Import views
# from myapps.views import (
#     FetchScriptView, InfoAPIView, LoginUserAPIView, RegisterUserAPIView, 
#     ProjectDetailAPIView, GenerateScriptAPIView, get_csrf_token, 
#     post_monitor_data, get_monitor_data
# )

# # Root welcome page
# def home(request):
#     return HttpResponse("Welcome to my Django app!")

# urlpatterns = [
#     # Root URL
#     path('', home, name='home'),  
#     path('admin/', admin.site.urls),  
    
#     # API Endpoints
#     path('api/info/', InfoAPIView.as_view(), name='get_info'),  
#     path('api/register/', RegisterUserAPIView.as_view(), name='register'),  
#     path('api/login/', LoginUserAPIView.as_view(), name='user_login'),  
#     path('api/projectdetails/', ProjectDetailAPIView.as_view(), name='project_detail_list'),  
#     path('api/projectdetails/<int:pk>/', ProjectDetailAPIView.as_view(), name='project_detail_detail'),  
#     path('api/projectdetails/<int:project_id>/scripts/', FetchScriptView.as_view(), name='fetch_script'),
#     path('api/generate-script/', GenerateScriptAPIView.as_view(), name='generate_script'),
#     path('api/fetch-script/<int:project_id>/<str:stage_id>/', FetchScriptView.as_view(), name='fetch_script'),
#     path("csrf/", get_csrf_token, name="get_csrf_token"),
#     path('monitor/post/', post_monitor_data, name='post_monitor_data'),  
#     path('monitor/get/', get_monitor_data, name='get_monitor_data'),  

#     # Favicon Handling
#     path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),  
# ]

# # Serve static files in development mode
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

# Import views
from myapps.views import (
    FetchScriptView, InfoAPIView, LoginUserAPIView, RegisterUserAPIView,
    ProjectDetailAPIView, GenerateScriptAPIView, get_csrf_token,
    post_monitor_data, get_monitor_data, check_email # Added check_email import
)

# Root welcome page
def home(request):
    return HttpResponse("Welcome to my Django app!")

urlpatterns = [
    # Root URL
    path('', home, name='home'),
    path('admin/', admin.site.urls),

    # API Endpoints
    path('api/info/', InfoAPIView.as_view(), name='get_info'),
    path('api/register/', RegisterUserAPIView.as_view(), name='register'),
    path('api/login/', LoginUserAPIView.as_view(), name='user_login'),
    path('api/projectdetails/', ProjectDetailAPIView.as_view(), name='project_detail_list'),
    path('api/projectdetails/<int:pk>/', ProjectDetailAPIView.as_view(), name='project_detail_detail'),
    path('api/projectdetails/<int:project_id>/scripts/', FetchScriptView.as_view(), name='fetch_script'),
    path('api/generate-script/', GenerateScriptAPIView.as_view(), name='generate_script'),
    path('api/fetch-script/<int:project_id>/<str:stage_id>/', FetchScriptView.as_view(), name='fetch_script'),
    path("csrf/", get_csrf_token, name="get_csrf_token"),
    path('monitor/post/', post_monitor_data, name='post_monitor_data'),
    path('monitor/get/', get_monitor_data, name='get_monitor_data'),
    path('api/check-email/', check_email, name='check_email'), # Added check_email url

    # Favicon Handling
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
]

# Serve static files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
