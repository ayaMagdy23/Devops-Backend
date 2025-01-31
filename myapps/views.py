from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView  # Make sure to import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PipelineStage, Script, Tool
from .serializers import ScriptSerializer, ToolSerializer  # Ensure these are defined
from django.http import HttpResponse

# ScriptAPIView now renders an HTML template
class ScriptAPIView(APIView):
    def get(self, request, stage, format=None):
        # Fetch the stage from the database
        stage_obj = get_object_or_404(PipelineStage, name__iexact=stage)

        # Query all scripts linked to this stage
        scripts = Script.objects.filter(stage=stage_obj)

        if scripts.exists():
            return render(request, 'scripts_list.html', {'scripts': scripts, 'stage': stage_obj})
        else:
            return HttpResponse("No scripts found for this stage.", status=404)

# ToolAPIView now renders an HTML template
class ToolAPIView(APIView):
    def get(self, request, stage, format=None):
        # Fetch the stage from the database
        stage_obj = get_object_or_404(PipelineStage, name__iexact=stage)

        # Query all tools linked to this stage
        tools = Tool.objects.filter(stage=stage_obj)

        if tools.exists():
            return render(request, 'tools_list.html', {'tools': tools, 'stage': stage_obj})
        else:
            return HttpResponse("No tools found for this stage.", status=404)

# New get_info view, you can render some template here as well
def get_info(request):
    return render(request, 'info.html', {'info': 'Here is some information'})
