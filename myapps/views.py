# views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PipelineStage, Script, Tool
from .serializers import ScriptSerializer, ToolSerializer  # Ensure these are defined
from django.http import JsonResponse

# Existing ScriptAPIView
class ScriptAPIView(APIView):
    def get(self, request, stage, format=None):
        # Fetch the stage from the database
        stage_obj = get_object_or_404(PipelineStage, name__iexact=stage)

        # Query all scripts linked to this stage
        scripts = Script.objects.filter(stage=stage_obj)

        if scripts.exists():
            serializer = ScriptSerializer(scripts, many=True)
            return Response({'scripts': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No scripts found for this stage.'}, status=status.HTTP_404_NOT_FOUND)

# Existing ToolAPIView
class ToolAPIView(APIView):
    def get(self, request, stage, format=None):
        # Fetch the stage from the database
        stage_obj = get_object_or_404(PipelineStage, name__iexact=stage)

        # Query all tools linked to this stage
        tools = Tool.objects.filter(stage=stage_obj)

        if tools.exists():
            serializer = ToolSerializer(tools, many=True)
            return Response({'tools': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No tools found for this stage.'}, status=status.HTTP_404_NOT_FOUND)

# New get_info view
def get_info(request):
    return JsonResponse({"info": "Here is some information"})
