from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Script, Tool, PipelineStage
from rest_framework import status

class InfoAPIView(APIView):
    def get(self, request):
        # A simple endpoint that returns a welcome message
        return Response({"message": "Welcome to the API!"}, status=200)

class ScriptAPIView(APIView):
    def get(self, request, stage):
        # Check if the stage exists in the database
        try:
            pipeline_stage = PipelineStage.objects.get(name=stage)
        except PipelineStage.DoesNotExist:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Retrieve all scripts associated with that stage
        scripts = Script.objects.filter(stage=pipeline_stage)
        
        # Return a list of scripts in the response
        script_data = [{
            'title': script.title,
            'description': script.description,
            'script_link': script.script_link
        } for script in scripts]
        
        return Response(script_data, status=status.HTTP_200_OK)

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
