# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from .models import Script, Tool, PipelineStage, ProjectDetail
# from .serializers import UserSerializer, ScriptSerializer, ToolSerializer, ProjectDetailSerializer

# # Info API View
# class InfoAPIView(APIView):
#     permission_classes = [permissions.AllowAny]
    
#     def get(self, request):
#         return Response({"message": "Welcome to the API!"}, status=status.HTTP_200_OK)

# # User Registration API View
# class RegisterUserAPIView(APIView):
#     permission_classes = [permissions.AllowAny]
    
#     def get(self, request):
#         """Retrieve all registered users."""
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """Register a new user."""
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "User created successfully!", "user_id": user.id}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Login API View
# class LoginUserAPIView(APIView):
#     permission_classes = [permissions.AllowAny]
    
#     def post(self, request):
#         """Authenticate user and login."""
#         username = request.data.get('username')
#         password = request.data.get('password')

#         if not username or not password:
#             return Response({"error": "Please provide both username and password."}, status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(username=username, password=password)

#         if user is not None:
#             return Response({"message": "Successfully signed in!"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid credentials. Please try again."}, status=status.HTTP_401_UNAUTHORIZED)

# # Script API View
# class ScriptAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         """Retrieve scripts based on project details."""
#         project_details = request.query_params
        
#         scripts = Script.objects.all()

#         # Filtering scripts based on the project details provided
#         project_type = project_details.get('project_type')
#         programming_language = project_details.get('programming_language')
#         framework = project_details.get('framework')
#         hosting_platform = project_details.get('hosting_platform')
#         deployment_type = project_details.get('deployment_type')
#         testing_needs = project_details.get('testing_needs')

#         if project_type:
#             scripts = scripts.filter(category__icontains=project_type)
#         if programming_language:
#             scripts = scripts.filter(category__icontains=programming_language)
#         if framework:
#             scripts = scripts.filter(category__icontains=framework)
#         if hosting_platform:
#             scripts = scripts.filter(category__icontains=hosting_platform)
#         if deployment_type:
#             scripts = scripts.filter(category__icontains=deployment_type)
#         if testing_needs:
#             scripts = scripts.filter(category__icontains=testing_needs)

#         # If any scripts match, return them, otherwise return an error
#         if scripts.exists():
#             return Response(ScriptSerializer(scripts, many=True).data, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "No matching scripts found."}, status=status.HTTP_404_NOT_FOUND)

#     def post(self, request):
#         """Create a new script."""
#         stage = request.data.get("stage")
#         try:
#             pipeline_stage = PipelineStage.objects.get(name=stage)
#             serializer = ScriptSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(stage=pipeline_stage)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except PipelineStage.DoesNotExist:
#             return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

# # Tool API View
# class ToolAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get(self, request, stage):
#         try:
#             pipeline_stage = PipelineStage.objects.get(name=stage)
#             tools = Tool.objects.filter(stage=pipeline_stage)
#             return Response(ToolSerializer(tools, many=True).data, status=status.HTTP_200_OK)
#         except PipelineStage.DoesNotExist:
#             return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

#     def post(self, request, stage):
#         try:
#             pipeline_stage = PipelineStage.objects.get(name=stage)
#             serializer = ToolSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(stage=pipeline_stage)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except PipelineStage.DoesNotExist:
#             return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

# # Project Detail API View
# class ProjectDetailAPIView(APIView):
#     def get(self, request):
#         """Retrieve all project details."""
#         project_details = ProjectDetail.objects.all()
#         serializer = ProjectDetailSerializer(project_details, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """Create a new project detail."""
#         serializer = ProjectDetailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         """Update an existing project detail."""
#         try:
#             project_detail = ProjectDetail.objects.get(pk=pk)
#         except ProjectDetail.DoesNotExist:
#             return Response({"error": "ProjectDetail not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = ProjectDetailSerializer(project_detail, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         """Delete a project detail."""
#         try:
#             project_detail = ProjectDetail.objects.get(pk=pk)
#         except ProjectDetail.DoesNotExist:
#             return Response({"error": "ProjectDetail not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         project_detail.delete()
#         return Response({"message": "Project detail deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# from django.http import JsonResponse
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from .models import Script, Tool, PipelineStage, ProjectDetail
# from .serializers import UserSerializer, ScriptSerializer, ToolSerializer, ProjectDetailSerializer

# # Info API View
# class InfoAPIView(APIView):
#     def get(self, request):
#         return Response({"message": "Welcome to the API!"}, status=200)

# # User Registration API View
# class RegisterUserAPIView(APIView):
#     def get(self, request):
#         """Retrieve all registered users."""
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """Register a new user."""
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "User created successfully!", "user_id": user.id}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Login API View
# class LoginUserAPIView(APIView):
#     def post(self, request):
#         """Login an existing user."""
#         username = request.data.get('username')
#         password = request.data.get('password')

#         if not username or not password:
#             return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Authenticate the user
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             return Response({"message": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# # Script API View
# class ScriptAPIView(APIView):
#     def get(self, request, stage):
#         try:
#             pipeline_stage = PipelineStage.objects.get(name=stage)
#         except PipelineStage.DoesNotExist:
#             return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         scripts = Script.objects.filter(stage=pipeline_stage)
#         script_data = [ScriptSerializer(script).data for script in scripts]
        
#         return Response(script_data, status=status.HTTP_200_OK)

#     def post(self, request, stage):
#         try:
#             pipeline_stage = PipelineStage.objects.get(name=stage)
#         except PipelineStage.DoesNotExist:
#             return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = ScriptSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(stage=pipeline_stage)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Tool API View
# class ToolAPIView(APIView):
#     def get(self, request, stage):
#         try:
#             pipeline_stage = PipelineStage.objects.get(name=stage)
#         except PipelineStage.DoesNotExist:
#             return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         tools = Tool.objects.filter(stage=pipeline_stage)
#         tool_data = [ToolSerializer(tool).data for tool in tools]
        
#         return Response(tool_data, status=status.HTTP_200_OK)

#     def post(self, request, stage):
#         try:
#             pipeline_stage = PipelineStage.objects.get(name=stage)
#         except PipelineStage.DoesNotExist:
#             return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = ToolSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(stage=pipeline_stage)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Project Detail API View
# class ProjectDetailAPIView(APIView):
#     def get(self, request):
#         """Retrieve all project details."""
#         project_details = ProjectDetail.objects.all()
#         serializer = ProjectDetailSerializer(project_details, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """Create a new project detail."""
#         data = request.data

#         # Extract IDs
#         selected_stage_id = data.pop('selected_stage', None)
#         script_id = data.pop('script', None)
#         tool_id = data.pop('tool', None)

#         serializer = ProjectDetailSerializer(data=data)
#         if serializer.is_valid():
#             project_detail = serializer.save()

#             # Assign selected_stage if provided
#             if selected_stage_id:
#                 project_detail.selected_stage = PipelineStage.objects.get(id=selected_stage_id)

#             # Assign script if provided
#             if script_id:
#                 project_detail.script = Script.objects.get(id=script_id)

#             # Assign tool if provided
#             if tool_id:
#                 project_detail.tool = Tool.objects.get(id=tool_id)

#             project_detail.save()

#             return Response(ProjectDetailSerializer(project_detail).data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         """Update an existing project detail."""
#         try:
#             project_detail = ProjectDetail.objects.get(pk=pk)
#         except ProjectDetail.DoesNotExist:
#             return Response({"error": "ProjectDetail not found"}, status=status.HTTP_404_NOT_FOUND)

#         data = request.data

#         # Extract IDs
#         selected_stage_id = data.pop('selected_stage', None)
#         script_id = data.pop('script', None)
#         tool_id = data.pop('tool', None)

#         serializer = ProjectDetailSerializer(project_detail, data=data)
#         if serializer.is_valid():
#             project_detail = serializer.save()

#             # Update selected_stage if provided
#             if selected_stage_id:
#                 project_detail.selected_stage = PipelineStage.objects.get(id=selected_stage_id)

#             # Update script if provided
#             if script_id:
#                 project_detail.script = Script.objects.get(id=script_id)

#             # Update tool if provided
#             if tool_id:
#                 project_detail.tool = Tool.objects.get(id=tool_id)

#             project_detail.save()

#             return Response(ProjectDetailSerializer(project_detail).data, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         """Delete a project detail."""
#         try:
#             project_detail = ProjectDetail.objects.get(pk=pk)
#         except ProjectDetail.DoesNotExist:
#             return Response({"error": "ProjectDetail not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         project_detail.delete()
#         return Response({"message": "Project detail deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# def get_script(request, project_id, stage_id): 
#     try:
#         project_detail = ProjectDetail.objects.get(id=project_id)
#         stage = PipelineStage.objects.get(id=stage_id)

#         # Get the script associated with this project and stage
#         script = Script.objects.filter(stage=stage).first()

#         if script:
#             return JsonResponse({"script_link": script.script_content}, status=200)
#         else:
#             return JsonResponse({"error": "Script not found for this stage."}, status=404)

#     except ProjectDetail.DoesNotExist:
#         return JsonResponse({"error": "Project not found."}, status=404)
#     except PipelineStage.DoesNotExist:
#         return JsonResponse({"error": "Stage not found."}, status=404)

# class FetchScriptView(APIView):
#     def get(self, request, project_id, stage_id):
#         try:
#             # Fetch the project details
#             project_detail = ProjectDetail.objects.get(id=project_id)
            
#             # Check if the project framework matches "Node.js" and the stage matches "Development"
#             if project_detail.framework == "Node.js" and stage_id == "development":
#                 # Find the script associated with the project and stage
#                 script = Script.objects.filter(project_detail=project_detail, stage__name="Development").first()
                
#                 if script:
#                     return Response({"script_content": script.script_content}, status=200)
#                 else:
#                     return Response({"error": "No Node.js script found for the Development stage."}, status=404)
#             else:
#                 return Response({"error": "No matching framework or stage found."}, status=404)
#         except ProjectDetail.DoesNotExist:
#             return Response({"error": "Project not found."}, status=404)
        

# from django.http import JsonResponse
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from .models import Script, Tool, PipelineStage, ProjectDetail
# from .serializers import UserSerializer, ScriptSerializer, ToolSerializer, ProjectDetailSerializer


# # Info API View
# class InfoAPIView(APIView):
#     def get(self, request):
#         return Response({"message": "Welcome to the API!"}, status=status.HTTP_200_OK)


# # User Registration API View
# class RegisterUserAPIView(APIView):
#     def get(self, request):
#         """Retrieve all registered users."""
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """Register a new user."""
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "User created successfully!", "user_id": user.id}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # Login API View
# class LoginUserAPIView(APIView):
#     def post(self, request):
#         """Login an existing user."""
#         username = request.data.get('username')
#         password = request.data.get('password')

#         if not username or not password:
#             return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Authenticate the user
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             return Response({"message": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# # Script API View
# class ScriptAPIView(APIView):
#     def get(self, request, stage):
#         try:
#             pipeline_stage = PipelineStage.objects.get(name=stage)
#         except PipelineStage.DoesNotExist:
#             return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

#         scripts = Script.objects.filter(stage=pipeline_stage)
#         script_data = [ScriptSerializer(script).data for script in scripts]

#         return Response(script_data, status=status.HTTP_200_OK)

#     def post(self, request, stage):
#         try:
#             pipeline_stage = PipelineStage.objects.get(name=stage)
#         except PipelineStage.DoesNotExist:
#             return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = ScriptSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(stage=pipeline_stage)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # Tool API View
# class ToolAPIView(APIView):
#     def get(self, request, stage):
#         try:
#             pipeline_stage = PipelineStage.objects.get(name=stage)
#         except PipelineStage.DoesNotExist:
#             return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

#         tools = Tool.objects.filter(stage=pipeline_stage)
#         tool_data = [ToolSerializer(tool).data for tool in tools]

#         return Response(tool_data, status=status.HTTP_200_OK)

#     def post(self, request, stage):
#         try:
#             pipeline_stage = PipelineStage.objects.get(name=stage)
#         except PipelineStage.DoesNotExist:
#             return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = ToolSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(stage=pipeline_stage)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # Project Detail API View
# class ProjectDetailAPIView(APIView):
#     def get(self, request):
#         """Retrieve all project details."""
#         project_details = ProjectDetail.objects.all()
#         serializer = ProjectDetailSerializer(project_details, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """Create a new project detail."""
#         data = request.data

#         # Extract IDs
#         selected_stage_id = data.pop('selected_stage', None)
#         script_id = data.pop('script', None)
#         tool_id = data.pop('tool', None)

#         serializer = ProjectDetailSerializer(data=data)
#         if serializer.is_valid():
#             project_detail = serializer.save()

#             # Assign selected_stage if provided
#             if selected_stage_id:
#                 project_detail.selected_stage = PipelineStage.objects.get(id=selected_stage_id)

#             # Assign script if provided
#             if script_id:
#                 project_detail.script = Script.objects.get(id=script_id)

#             # Assign tool if provided
#             if tool_id:
#                 project_detail.tool = Tool.objects.get(id=tool_id)

#             project_detail.save()

#             return Response(ProjectDetailSerializer(project_detail).data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         """Update an existing project detail."""
#         try:
#             project_detail = ProjectDetail.objects.get(pk=pk)
#         except ProjectDetail.DoesNotExist:
#             return Response({"error": "ProjectDetail not found"}, status=status.HTTP_404_NOT_FOUND)

#         data = request.data

#         # Extract IDs
#         selected_stage_id = data.pop('selected_stage', None)
#         script_id = data.pop('script', None)
#         tool_id = data.pop('tool', None)

#         serializer = ProjectDetailSerializer(project_detail, data=data)
#         if serializer.is_valid():
#             project_detail = serializer.save()

#             # Update selected_stage if provided
#             if selected_stage_id:
#                 project_detail.selected_stage = PipelineStage.objects.get(id=selected_stage_id)

#             # Update script if provided
#             if script_id:
#                 project_detail.script = Script.objects.get(id=script_id)

#             # Update tool if provided
#             if tool_id:
#                 project_detail.tool = Tool.objects.get(id=tool_id)

#             project_detail.save()

#             return Response(ProjectDetailSerializer(project_detail).data, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         """Delete a project detail."""
#         try:
#             project_detail = ProjectDetail.objects.get(pk=pk)
#         except ProjectDetail.DoesNotExist:
#             return Response({"error": "ProjectDetail not found"}, status=status.HTTP_404_NOT_FOUND)

#         project_detail.delete()
#         return Response({"message": "Project detail deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# # Fetch Script for Project and Stage
# class FetchScriptView(APIView):
#     def get(self, request, project_id, stage_id):
#         try:
#             # Fetch the project details
#             project_detail = ProjectDetail.objects.get(id=project_id)

#             # Check if the project framework matches "Node.js" and the stage matches "Development"
#             if project_detail.framework == "Node.js" and stage_id == "development":
#                 # Find the script associated with the project and stage
#                 script = Script.objects.filter(project_detail=project_detail, stage__name="Development").first()

#                 if script:
#                     return Response({"script_content": script.script_content}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"error": "No Node.js script found for the Development stage."}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 return Response({"error": "No matching framework or stage found."}, status=status.HTTP_404_NOT_FOUND)

#         except ProjectDetail.DoesNotExist:
#             return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

#         except PipelineStage.DoesNotExist:
#             return Response({"error": "Stage not found."}, status=status.HTTP_404_NOT_FOUND)

# from django.http import JsonResponse
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.middleware.csrf import get_token  # ✅ Added missing import
# from .models import Script, Tool, PipelineStage, ProjectDetail, MonitoringData
# from .serializers import (
#     UserSerializer, ScriptSerializer, ToolSerializer, ProjectDetailSerializer, MonitoringDataSerializer
# )
# from .services.openai_service import generate_pipeline_script
# from django.contrib.auth.hashers import make_password
# from supabase import create_client
# from django.conf import settings
# import logging

# from django.http import JsonResponse
# import dns.resolver

# from rest_framework_simplejwt.tokens import RefreshToken

# # Info API View
# class InfoAPIView(APIView):
#     def get(self, request):
#         return Response({"message": "Welcome to the API!"}, status=status.HTTP_200_OK)


# # User Registration API View
# # Set up logging
# logger = logging.getLogger(__name__)

# class RegisterUserAPIView(APIView):
#     def post(self, request):
#         """Register a new user."""
#         data = request.data

#         try:
#             # Check if user already exists by email
#             existing_user = User.objects.filter(email=data.get("email")).first()
#             if existing_user:
#                 return Response({"error": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

#             # Check if username already exists
#             existing_username = User.objects.filter(username=data.get("username")).first()
#             if existing_username:
#                 return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

#             # Create the new user
#             user = User.objects.create_user(
#                 username=data["username"],
#                 email=data["email"],
#                 password=data["password"]  # Django will hash the password automatically
#             )

#             # Return a success message
#             return Response({"message": "User registered successfully!", "user_id": user.id}, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# # Login API View
# class LoginUserAPIView(APIView):
#     def post(self, request):
#         print("Request Data:", request.data)  # Debugging line

#         # Get username and password from the request
#         username = request.data.get('username')
#         password = request.data.get('password')

#         # Check if username and password are provided
#         if not username or not password:
#             return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Authenticate user using username and password
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             # Generate JWT tokens if authentication is successful
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "message": "Login successful",
#                 "user_id": user.id,
#                 "access_token": str(refresh.access_token),
#                 "refresh_token": str(refresh)
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# # Project Detail API View
# class ProjectDetailAPIView(APIView):
#     def get(self, request):
#         project_details = ProjectDetail.objects.all()
#         serializer = ProjectDetailSerializer(project_details, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         data = request.data
#         selected_stage_id = data.pop('selected_stage', None)
#         script_id = data.pop('script', None)
#         tool_id = data.pop('tool', None)

#         serializer = ProjectDetailSerializer(data=data)
#         if serializer.is_valid():
#             project_detail = serializer.save()

#             if selected_stage_id:
#                 project_detail.selected_stage = PipelineStage.objects.get(id=selected_stage_id)
#             if script_id:
#                 project_detail.script = Script.objects.get(id=script_id)
#             if tool_id:
#                 project_detail.tool = Tool.objects.get(id=tool_id)

#             project_detail.save()
#             return Response(ProjectDetailSerializer(project_detail).data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # Generate Script API View
# class GenerateScriptAPIView(APIView):
#     @method_decorator(csrf_exempt)  # ✅ Disable CSRF for this view
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request):
#         user_inputs = request.data
#         script = generate_pipeline_script(user_inputs)
#         return Response({"script": script}, status=status.HTTP_200_OK)


# # Fetch Script API View
# class FetchScriptView(APIView):
#     def get(self, request, project_id, stage_id):
#         try:
#             project_detail = ProjectDetail.objects.get(id=project_id)
#             stage = PipelineStage.objects.filter(name=stage_id).first()

#             if not stage:
#                 return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

#             script = Script.objects.filter(project_detail=project_detail, stage=stage).first()
#             if script:
#                 return Response({"script_content": script.script_content}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "No script found for the given stage."}, status=status.HTTP_404_NOT_FOUND)

#         except ProjectDetail.DoesNotExist:
#             return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)


# # CSRF Token Retrieval API View
# def get_csrf_token(request):
#     try:
#         csrf_token = get_token(request)
#         return JsonResponse({"csrfToken": csrf_token}, status=status.HTTP_200_OK)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# # Monitoring Data API Views
# @csrf_exempt  # ✅ Disable CSRF for testing; use authentication in production
# def post_monitor_data(request):
#     if request.method == 'POST':
#         try:
#             data = request.data  # ✅ Use Django REST Framework's request parsing

#             cpu_usage = data.get('cpu_usage')
#             memory_usage = data.get('memory_usage')
#             network_usage = data.get('network_usage')
#             disk_usage = data.get('disk_usage')

#             # Validate required fields
#             if None in (cpu_usage, memory_usage, network_usage, disk_usage):
#                 return JsonResponse({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

#             # Save data to database
#             MonitoringData.objects.create(
#                 cpu_usage=cpu_usage,
#                 memory_usage=memory_usage,
#                 network_usage=network_usage,
#                 disk_usage=disk_usage
#             )

#             return JsonResponse({"message": "Data received successfully"}, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# @api_view(['GET'])
# def get_monitor_data(request):
#     try:
#         monitoring_entries = MonitoringData.objects.all().order_by('-timestamp')[:10]  # Get latest 10 entries
#         serializer = MonitoringDataSerializer(monitoring_entries, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# from rest_framework.response import Response
# from rest_framework.decorators import api_view
















# from django.http import JsonResponse
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.middleware.csrf import get_token
# from .models import Script, Tool, PipelineStage, ProjectDetail, MonitoringData
# from .serializers import (
#     UserSerializer, ScriptSerializer, ToolSerializer, ProjectDetailSerializer, MonitoringDataSerializer
# )
# from .services.openai_service import generate_pipeline_script
# from django.contrib.auth.hashers import make_password
# from supabase import create_client
# from django.conf import settings
# import logging
# import dns.resolver
# from rest_framework_simplejwt.tokens import RefreshToken

# # Info API View
# class InfoAPIView(APIView):
#     def get(self, request):
#         return Response({"message": "Welcome to the API!"}, status=status.HTTP_200_OK)

# # User Registration API View
# logger = logging.getLogger(__name__)

# class RegisterUserAPIView(APIView):
#     def post(self, request):
#         """Register a new user."""
#         data = request.data

#         try:
#             # Check if user already exists by email
#             existing_user = User.objects.filter(email=data.get("email")).first()
#             if existing_user:
#                 return Response({"error": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

#             # Check if username already exists
#             existing_username = User.objects.filter(username=data.get("username")).first()
#             if existing_username:
#                 return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

#             # Create the new user
#             user = User.objects.create_user(
#                 username=data["username"],
#                 email=data["email"],
#                 password=data["password"]
#             )

#             # Return a success message
#             return Response({"message": "User registered successfully!", "user_id": user.id}, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# # Login API View
# class LoginUserAPIView(APIView):
#     def post(self, request):
#         print("Request Data:", request.data)  # Debugging line

#         # Get username and password from the request
#         username = request.data.get('username')
#         password = request.data.get('password')

#         # Check if username and password are provided
#         if not username or not password:
#             return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Authenticate user using username and password
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             # Generate JWT tokens if authentication is successful
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "message": "Login successful",
#                 "user_id": user.id,
#                 "access_token": str(refresh.access_token),
#                 "refresh_token": str(refresh)
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# # Project Detail API View
# class ProjectDetailAPIView(APIView):
#     def get(self, request):
#         project_details = ProjectDetail.objects.all()
#         serializer = ProjectDetailSerializer(project_details, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         data = request.data
#         selected_stage_id = data.pop('selected_stage', None)
#         script_id = data.pop('script', None)
#         tool_id = data.pop('tool', None)

#         serializer = ProjectDetailSerializer(data=data)
#         if serializer.is_valid():
#             project_detail = serializer.save()

#             if selected_stage_id:
#                 project_detail.selected_stage = PipelineStage.objects.get(id=selected_stage_id)
#             if script_id:
#                 project_detail.script = Script.objects.get(id=script_id)
#             if tool_id:
#                 project_detail.tool = Tool.objects.get(id=tool_id)

#             project_detail.save()
#             return Response(ProjectDetailSerializer(project_detail).data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Generate Script API View
# class GenerateScriptAPIView(APIView):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request):
#         user_inputs = request.data
#         script = generate_pipeline_script(user_inputs)
#         return Response({"script": script}, status=status.HTTP_200_OK)

# # Fetch Script API View
# class FetchScriptView(APIView):
#     def get(self, request, project_id, stage_id):
#         try:
#             project_detail = ProjectDetail.objects.get(id=project_id)
#             stage = PipelineStage.objects.filter(name=stage_id).first()

#             if not stage:
#                 return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

#             script = Script.objects.filter(project_detail=project_detail, stage=stage).first()
#             if script:
#                 return Response({"script_content": script.script_content}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "No script found for the given stage."}, status=status.HTTP_404_NOT_FOUND)

#         except ProjectDetail.DoesNotExist:
#             return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

# # CSRF Token Retrieval API View
# def get_csrf_token(request):
#     try:
#         csrf_token = get_token(request)
#         return JsonResponse({"csrfToken": csrf_token}, status=status.HTTP_200_OK)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# # Monitoring Data API Views
# @csrf_exempt
# def post_monitor_data(request):
#     if request.method == 'POST':
#         try:
#             data = request.data

#             cpu_usage = data.get('cpu_usage')
#             memory_usage = data.get('memory_usage')
#             network_usage = data.get('network_usage')
#             disk_usage = data.get('disk_usage')

#             # Validate required fields
#             if None in (cpu_usage, memory_usage, network_usage, disk_usage):
#                 return JsonResponse({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

#             # Save data to database
#             MonitoringData.objects.create(
#                 cpu_usage=cpu_usage,
#                 memory_usage=memory_usage,
#                 network_usage=network_usage,
#                 disk_usage=disk_usage
#             )

#             return JsonResponse({"message": "Data received successfully"}, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# @api_view(['GET'])
# def get_monitor_data(request):
#     try:
#         monitoring_entries = MonitoringData.objects.all().order_by('-timestamp')[:10]
#         serializer = MonitoringDataSerializer(monitoring_entries, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# # Email Validation View
# @api_view(['POST'])
# def check_email(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         if not email:
#             return Response({'isValid': False}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             domain = email.split('@')[1]
#             mx_records = dns.resolver.resolve(domain, 'MX')
#             is_valid = len(mx_records) > 0
#             return Response({'isValid': is_valid}, status=status.HTTP_200_OK)
#         except dns.resolver.NXDOMAIN:
#             return Response({'isValid': False}, status=status.HTTP_200_OK)
#         except Exception as e:
#             print(f"Error checking email: {e}")
#             return Response({'isValid': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     else:
#         return Response({'isValid': False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
#     from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated  # Ensure user is authenticated
# from .models import ProjectDetail
# from .serializers import ProjectDetailSerializer

# class PastProjectsAPIView(APIView):
#     permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

#     def get(self, request):
#         # Fetch all projects for the logged-in user
#         user = request.user  # Get the current authenticated user
#         projects = ProjectDetail.objects.filter(user=user)  # Filter projects by user
#         serializer = ProjectDetailSerializer(projects, many=True)  # Serialize the data
#         return Response(serializer.data, status=status.HTTP_200_OK)