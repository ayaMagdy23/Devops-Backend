from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Script, Tool, PipelineStage
from rest_framework import status
from .serializers import UserSerializer, ScriptSerializer

class InfoAPIView(APIView):
    def get(self, request):
        # A simple endpoint that returns a welcome message
        return Response({"message": "Welcome to the API!"}, status=200)

class RegisterUserAPIView(APIView):
    # def get(self, request):
    #     """Retrieve all registered users."""
    #     users = User.objects.all()
    #     serializer = UserSerializer(users, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully!", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ScriptAPIView(APIView):
    def get(self, request, stage):
        # Check if the stage exists in the database
        try:
            pipeline_stage = PipelineStage.objects.get(name=stage)
        except PipelineStage.DoesNotExist:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Retrieve all scripts associated with that stage>
        scripts = Script.objects.filter(stage=pipeline_stage)
        
        # Return a list of scripts in the response
        script_data = [{
            'title': script.title,
            'description': script.description,
            'script': script.script
        } for script in scripts]
        
        return Response(script_data, status=status.HTTP_200_OK)
    
    def post(self, request, stage):
        # Validate if the stage exists
        try:
            pipeline_stage = PipelineStage.objects.get(name=stage)
        except PipelineStage.DoesNotExist:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize and validate data
        serializer = ScriptSerializer(data=request.data)
        if serializer.is_valid():
            # Save script with the retrieved stage
            serializer.save(stage=pipeline_stage)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ToolAPIView(APIView):
    def get(self, request, stage):
        # Check if the stage exists in the database
        try:
            pipeline_stage = PipelineStage.objects.get(name=stage)
        except PipelineStage.DoesNotExist:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Retrieve all tools associated with that stage
        tools = Tool.objects.filter(stage=pipeline_stage)
        
        # Return a list of tools in the response
        tool_data = [{
            'name': tool.name,
            'description': tool.description,
            'url': tool.url
        } for tool in tools]
        
        return Response(tool_data, status=status.HTTP_200_OK)
