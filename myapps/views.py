
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import MonitoringData
from myproject import settings
from .models import Script, SystemUsage, Tool, PipelineStage, ProjectDetail
from .serializers import UserSerializer, ScriptSerializer, ToolSerializer, ProjectDetailSerializer
from .services.openai_service import generate_pipeline_script
from .models import MonitoringData
from .serializers import MonitoringDataSerializer
from django.middleware.csrf import get_token
import json
from django.http import FileResponse
import os
from rest_framework.renderers import TemplateHTMLRenderer
import openai
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny

# Info API View
class InfoAPIView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the API!"}, status=200)

# User Registration API View
class RegisterUserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully!", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login API View
class LoginUserAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            return Response({"message": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Script API View
class ScriptAPIView(APIView):
    def get(self, request, stage):
        try:
            pipeline_stage = PipelineStage.objects.get(name=stage)
        except PipelineStage.DoesNotExist:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)
        
        scripts = Script.objects.filter(stage=pipeline_stage)
        script_data = [ScriptSerializer(script).data for script in scripts]
        
        return Response(script_data, status=status.HTTP_200_OK)

    def post(self, request, stage):
        try:
            pipeline_stage = PipelineStage.objects.get(name=stage)
        except PipelineStage.DoesNotExist:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ScriptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(stage=pipeline_stage)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Tool API View
class ToolAPIView(APIView):
    def get(self, request, stage):
        try:
            pipeline_stage = PipelineStage.objects.get(name=stage)
        except PipelineStage.DoesNotExist:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)
        
        tools = Tool.objects.filter(stage=pipeline_stage)
        tool_data = [ToolSerializer(tool).data for tool in tools]
        
        return Response(tool_data, status=status.HTTP_200_OK)

    def post(self, request, stage):
        try:
            pipeline_stage = PipelineStage.objects.get(name=stage)
        except PipelineStage.DoesNotExist:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ToolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(stage=pipeline_stage)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = [AllowAny]  # Add this line
    
    def post(self, request):
        try:
            # Validate required fields
            required_fields = ['stage', 'framework', 'language', 'hosting_platform']
            missing_fields = [field for field in required_fields if field not in request.data]
            
            if missing_fields:
                return Response(
                    {"error": f"Missing required fields: {', '.join(missing_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify OpenAI configuration
            if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
                return Response(
                    {"error": "OpenAI API key not configured"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Generate script
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a DevOps expert."},
                    {"role": "user", "content": self._build_prompt(request.data)}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            script_content = response.choices[0].message.content
            
            # Return JSON response
            return Response({"script": script_content}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _build_prompt(self, inputs):
        """Construct the prompt for OpenAI"""
        return f"""
        Generate a {inputs['stage']} stage script for:
        - Language: {inputs['language']}
        - Framework: {inputs['framework']}
        - Platform: {inputs['hosting_platform']}
        - Deployment type: {inputs.get('deployment_type', 'container')}
        
        The script should:
        1. Follow best practices
        2. Include error handling
        3. Have clear comments
        4. Be specific to the target platform
        
        Output ONLY the script content with no additional text or explanations.
        """
    
# Fetch Script API View
class FetchScriptView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, project_id, stage_id):
        try:
            project_detail = ProjectDetail.objects.get(id=project_id)
            if project_detail.framework == "Node.js" and stage_id == "development":
                script = Script.objects.filter(project_detail=project_detail, stage__name="Development").first()
                if script:
                    return Response({"script_content": script.script_content}, template_name="script_detail.html")
                else:
                    return Response({"error": "No Node.js script found for the Development stage."}, status=404, template_name="error.html")
            else:
                return Response({"error": "No matching framework or stage found."}, status=404, template_name="error.html")
        except ProjectDetail.DoesNotExist:
            return Response({"error": "Project not found."}, status=404, template_name="error.html")

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})



@csrf_exempt
def post_monitor_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON request body
            print(f"Received data: {data}")  # Debugging print

            # Create new entry in MonitoringData model
            monitoring_data = MonitoringData.objects.create(
                cpu_usage=data['cpu_usage'],
                memory_usage=data['memory_usage'],
                disk_usage=data['disk_usage'],
                network_usage=data['network_usage'],
            )
            print(f"Saved data to DB: {monitoring_data}")  # Debugging print

            return JsonResponse({"status": "success", "data": data}, status=201)
        except Exception as e:
            print(f"Error: {e}")  # Debugging print
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=405)

@api_view(['GET'])
def get_monitor_data(request):
    monitoring_entries = MonitoringData.objects.all().order_by('-timestamp')[:10]  # Get latest 10 entries
    serializer = MonitoringDataSerializer(monitoring_entries, many=True)
    return Response(serializer.data)

@csrf_exempt
@csrf_exempt
def receive_metrics(request):
    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            print(f"Received data: {data}")  # Debugging print

            # Save the data to the SystemUsage model
            system_usage = SystemUsage.objects.create(
                cpu_usage=data.get('cpu_usage', 0),
                memory_usage=data.get('memory_usage', 0),
                disk_usage=data.get('disk_usage', 0),
                network_sent=data.get('network_sent', 0),
                network_received=data.get('network_received', 0)
            )

            # Debugging print for saved data
            print(f"Saved data to DB: {system_usage}")

            # Respond with success
            return JsonResponse({"message": "Metrics received successfully!"}, status=200)
        
        except json.JSONDecodeError:
            # Handle JSON decoding errors
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            # Catch other exceptions
            return JsonResponse({"error": str(e)}, status=400)
    
    # If the request method is not POST
    return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)
def download_monitor_script(request):
    # Get the absolute path of the monitor.py file
    script_path = os.path.join(settings.BASE_DIR, 'scripts', 'monitor.py')
    
    try:
        return FileResponse(open(script_path, "rb"), as_attachment=True, filename="monitor.py")
    except FileNotFoundError:
        return JsonResponse({"error": "The requested file does not exist."}, status=404)
    
    