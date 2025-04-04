from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from .models import Script, Tool, PipelineStage, ProjectDetail, MonitoringData
from .serializers import (
    UserSerializer, ScriptSerializer, ToolSerializer, ProjectDetailSerializer, MonitoringDataSerializer
)
from .services.openai_service import generate_pipeline_script
from django.contrib.auth.hashers import make_password
from supabase import create_client
from django.conf import settings
import logging
import dns.resolver
from rest_framework_simplejwt.tokens import RefreshToken

# Info API View
class InfoAPIView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the API!"}, status=status.HTTP_200_OK)

# User Registration API View
logger = logging.getLogger(__name__)

class RegisterUserAPIView(APIView):
    def post(self, request):
        """Register a new user."""
        data = request.data

        try:
            # Check if user already exists by email
            existing_user = User.objects.filter(email=data.get("email")).first()
            if existing_user:
                return Response({"error": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if username already exists
            existing_username = User.objects.filter(username=data.get("username")).first()
            if existing_username:
                return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the new user
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"]
            )

            # Return a success message
            return Response({"message": "User registered successfully!", "user_id": user.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Login API View
class LoginUserAPIView(APIView):
    def post(self, request):
        print("Request Data:", request.data)  # Debugging line

        # Get username and password from the request
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if username and password are provided
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user using username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Generate JWT tokens if authentication is successful
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "user_id": user.id,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Project Detail API View
class ProjectDetailAPIView(APIView):
    def get(self, request):
        project_details = ProjectDetail.objects.all()
        serializer = ProjectDetailSerializer(project_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        selected_stage_id = data.pop('selected_stage', None)
        script_id = data.pop('script', None)
        tool_id = data.pop('tool', None)

        serializer = ProjectDetailSerializer(data=data)
        if serializer.is_valid():
            project_detail = serializer.save()

            if selected_stage_id:
                project_detail.selected_stage = PipelineStage.objects.get(id=selected_stage_id)
            if script_id:
                project_detail.script = Script.objects.get(id=script_id)
            if tool_id:
                project_detail.tool = Tool.objects.get(id=tool_id)

            project_detail.save()
            return Response(ProjectDetailSerializer(project_detail).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Generate Script API View
class GenerateScriptAPIView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        user_inputs = request.data
        script = generate_pipeline_script(user_inputs)
        return Response({"script": script}, status=status.HTTP_200_OK)

# Fetch Script API View
class FetchScriptView(APIView):
    def get(self, request, project_id, stage_id):
        try:
            project_detail = ProjectDetail.objects.get(id=project_id)
            stage = PipelineStage.objects.filter(name=stage_id).first()

            if not stage:
                return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

            script = Script.objects.filter(project_detail=project_detail, stage=stage).first()
            if script:
                return Response({"script_content": script.script_content}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No script found for the given stage."}, status=status.HTTP_404_NOT_FOUND)

        except ProjectDetail.DoesNotExist:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

# CSRF Token Retrieval API View
def get_csrf_token(request):
    try:
        csrf_token = get_token(request)
        return JsonResponse({"csrfToken": csrf_token}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Monitoring Data API Views
@csrf_exempt
def post_monitor_data(request):
    if request.method == 'POST':
        try:
            data = request.data

            cpu_usage = data.get('cpu_usage')
            memory_usage = data.get('memory_usage')
            network_usage = data.get('network_usage')
            disk_usage = data.get('disk_usage')

            # Validate required fields
            if None in (cpu_usage, memory_usage, network_usage, disk_usage):
                return JsonResponse({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            # Save data to database
            MonitoringData.objects.create(
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                network_usage=network_usage,
                disk_usage=disk_usage
            )

            return JsonResponse({"message": "Data received successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def get_monitor_data(request):
    try:
        monitoring_entries = MonitoringData.objects.all().order_by('-timestamp')[:10]
        serializer = MonitoringDataSerializer(monitoring_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Email Validation View
@api_view(['POST'])
def check_email(request):
    if request.method == 'POST':
        email = request.data.get('email')
        if not email:
            return Response({'isValid': False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            domain = email.split('@')[1]
            mx_records = dns.resolver.resolve(domain, 'MX')
            is_valid = len(mx_records) > 0
            return Response({'isValid': is_valid}, status=status.HTTP_200_OK)
        except dns.resolver.NXDOMAIN:
            return Response({'isValid': False}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error checking email: {e}")
            return Response({'isValid': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'isValid': False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  # Ensure user is authenticated
from .models import ProjectDetail
from .serializers import ProjectDetailSerializer

class PastProjectsAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        # Fetch all projects for the logged-in user
        user = request.user  # Get the current authenticated user
        projects = ProjectDetail.objects.filter(user=user)  # Filter projects by user
        serializer = ProjectDetailSerializer(projects, many=True)  # Serialize the data
        return Response(serializer.data, status=status.HTTP_200_OK)