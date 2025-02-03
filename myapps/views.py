from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Script, Tool, PipelineStage, ProjectDetail
from .serializers import UserSerializer, ScriptSerializer, ToolSerializer, ProjectDetailSerializer
from django.contrib.auth.models import User

# Info API View
class InfoAPIView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the API!"}, status=200)

# User Registration API View
class RegisterUserAPIView(APIView):
    def get(self, request):
        """Retrieve all registered users."""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Register a new user."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully!", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        """Retrieve all project details."""
        project_details = ProjectDetail.objects.all()
        serializer = ProjectDetailSerializer(project_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new project detail."""
        serializer = ProjectDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Update an existing project detail."""
        try:
            project_detail = ProjectDetail.objects.get(pk=pk)
        except ProjectDetail.DoesNotExist:
            return Response({"error": "ProjectDetail not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectDetailSerializer(project_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a project detail."""
        try:
            project_detail = ProjectDetail.objects.get(pk=pk)
        except ProjectDetail.DoesNotExist:
            return Response({"error": "ProjectDetail not found"}, status=status.HTTP_404_NOT_FOUND)
        
        project_detail.delete()
        return Response({"message": "Project detail deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
