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

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, HttpResponseNotFound
from myapps import views
from myapps.views import FetchScriptView, InfoAPIView, LoginUserAPIView, RegisterUserAPIView, ProjectDetailAPIView ,GenerateScriptAPIView,get_csrf_token
# , GenerateScriptAPIView,CreateProjectView


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
    path('api/register/', RegisterUserAPIView.as_view(), name='register'),  # API for user registration
    path('api/login/', LoginUserAPIView.as_view(), name='user_login'),  # API for user login
    path('api/projectdetails/', ProjectDetailAPIView.as_view(), name='project_detail_list'),  # API to get all project details
    path('api/projectdetails/<int:pk>/', ProjectDetailAPIView.as_view(), name='project_detail_detail'),  # API for project detail by ID
    # path('api/get_script/<int:project_id>/<int:stage_id>/', views.get_script, name='get_script'),
   path('api/projectdetails/<int:project_id>/scripts/', FetchScriptView.as_view(), name='fetch_script'),
    # path('api/generate_script/', GenerateScriptAPIView.as_view(), name='generate_script'),  # API for generating scripts using OpenAI
    # path('api/create_project/', CreateProjectView.as_view(), name='create_project'),
    path('api/generate-script/', GenerateScriptAPIView.as_view(), name='generate-script'),
    path('api/fetch-script/<int:project_id>/<str:stage_id>/', FetchScriptView.as_view(), name='fetch_script'),
    path("csrf/", get_csrf_token, name="get_csrf_token"),
]
