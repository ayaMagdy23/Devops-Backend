from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Script, Tool, ProjectDetail, PipelineStage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ['title', 'description', 'script', 'category', 'stage']

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['name', 'description', 'url', 'stage']

class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetail
        fields = ['project_name', 'selected_stage', 'selected_option', 'script', 'tool', 'deployment_type', 
                  'framework', 'hosting_platform', 'programming_language', 'project_type', 'testing_needs']
