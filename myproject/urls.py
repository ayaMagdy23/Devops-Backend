# from django.contrib import admin
# from django.urls import path
# from django.http import HttpResponse, HttpResponseNotFound
# from myapps import views
# from myapps.views import FetchScriptView, InfoAPIView, LoginUserAPIView, RegisterUserAPIView, ProjectDetailAPIView ,GenerateScriptAPIView, download_monitor_script,get_csrf_token,post_monitor_data, get_monitor_data
# # , GenerateScriptAPIView,CreateProjectView
# from myapps.views import receive_metrics



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
#     path('api/register/', RegisterUserAPIView.as_view(), name='register'),  # API for user registration
#     path('api/login/', LoginUserAPIView.as_view(), name='user_login'),  # API for user login
#     path('api/projectdetails/', ProjectDetailAPIView.as_view(), name='project_detail_list'),  # API to get all project details
#     path('api/projectdetails/<int:pk>/', ProjectDetailAPIView.as_view(), name='project_detail_detail'),  # API for project detail by ID
#    path('api/projectdetails/<int:project_id>/scripts/', FetchScriptView.as_view(), name='fetch_script'),
#     path('api/generate-script/', GenerateScriptAPIView.as_view(), name='generate-script'),
#     path('api/fetch-script/<int:project_id>/<str:stage_id>/', FetchScriptView.as_view(), name='fetch_script'),
#     path("get-csrf-token/", get_csrf_token, name="get_csrf_token"),
#     path('api/monitoring/', views.receive_metrics, name='receive_metrics'),
#     path('api/post-monitor-data/', views.post_monitor_data, name='post_monitor_data'),
#     path('download-monitor/', views.download_monitor_script, name='download_monitor_script'),
# ]

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, HttpResponseNotFound
from myapps import views
from myapps.views import FetchScriptView, InfoAPIView, LoginUserAPIView, ProjectDetailAPIView ,GenerateScriptAPIView, download_monitor_script,get_csrf_token,post_monitor_data, get_monitor_data, RegisterView # Import RegisterView
# , GenerateScriptAPIView,CreateProjectView
from myapps.views import receive_metrics

# Define a simple view for the root URL
def home(request):
    return HttpResponse("Welcome to my Django app!")

# Define the favicon handler
def favicon(request):
    return HttpResponseNotFound()

urlpatterns = [
    path('', home, name='home'),   # Root URL
    path('admin/', admin.site.urls),   # Django admin panel
    path('favicon.ico', favicon),   # Handle favicon.ico requests

    # API Routes
    path('api/info/', InfoAPIView.as_view(), name='get_info'),   # API to retrieve info
    path('api/register/', RegisterView.as_view(), name='register'),   # API for user registration (using the correct view)
    path('api/login/', LoginUserAPIView.as_view(), name='user_login'),   # API for user login
    path('api/projectdetails/', ProjectDetailAPIView.as_view(), name='project_detail_list'),   # API to get all project details
    path('api/projectdetails/<int:pk>/', ProjectDetailAPIView.as_view(), name='project_detail_detail'),   # API for project detail by ID
   path('api/projectdetails/<int:project_id>/scripts/', FetchScriptView.as_view(), name='fetch_script'),
    path('api/generate-script/', GenerateScriptAPIView.as_view(), name='generate-script'),
    path('api/fetch-script/<int:project_id>/<str:stage_id>/', FetchScriptView.as_view(), name='fetch_script'),
    path("get-csrf-token/", get_csrf_token, name="get_csrf_token"),
    path('api/monitoring/', views.receive_metrics, name='receive_metrics'),
    path('api/post-monitor-data/', views.post_monitor_data, name='post_monitor_data'),
    path('download-monitor/', views.download_monitor_script, name='download_monitor_script'),
   
]