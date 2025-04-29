# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Script, Tool, ProjectDetail, PipelineStage

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)  # Ensure password is not exposed

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']

#     def create(self, validated_data):
#         """Create a new user with hashed password."""
#         user = User.objects.create_user(**validated_data)
#         return user


# class PipelineStageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PipelineStage
#         fields = ['id', 'name']


# class ScriptSerializer(serializers.ModelSerializer):
#     stage = PipelineStageSerializer(read_only=True)

#     class Meta:
#         model = Script
#         fields = ['id', 'title', 'description', 'script', 'category', 'stage']


# class ToolSerializer(serializers.ModelSerializer):
#     stage = PipelineStageSerializer(read_only=True)

#     class Meta:
#         model = Tool
#         fields = ['id', 'name', 'description', 'url', 'stage']


# class ProjectDetailSerializer(serializers.ModelSerializer):
#     selected_stage = PipelineStageSerializer(read_only=True)
#     script = ScriptSerializer(read_only=True)
#     tool = ToolSerializer(read_only=True)

#     class Meta:
#         model = ProjectDetail
#         fields = [
#             'id', 'project_name', 'selected_stage', 'selected_option', 'script', 'tool', 
#             'deployment_type', 'framework', 'hosting_platform', 'programming_language', 
#             'project_type', 'testing_needs'
#         ]

# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Script, Tool, ProjectDetail, PipelineStage, GeneratedScript

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)  # Ensure password is not exposed

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']

#     def create(self, validated_data):
#         """Create a new user with hashed password."""
#         user = User.objects.create_user(**validated_data)
#         return user


# class PipelineStageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PipelineStage
#         fields = ['id', 'name']


# class ScriptSerializer(serializers.ModelSerializer):
#     stage = PipelineStageSerializer(read_only=True)

#     class Meta:
#         model = Script
#         fields = ['id', 'title', 'description', 'script_content', 'category', 'stage']


# class ToolSerializer(serializers.ModelSerializer):
#     stage = PipelineStageSerializer(read_only=True)

#     class Meta:
#         model = Tool
#         fields = ['id', 'name', 'description', 'url', 'stage']


# class ProjectDetailSerializer(serializers.ModelSerializer):
#     selected_stage = PipelineStageSerializer(read_only=True)
#     script = ScriptSerializer(read_only=True)  # If you want to include the script in the response
#     tool = ToolSerializer(read_only=True)

#     class Meta:
#         model = ProjectDetail
#         fields = [
#             'id', 'project_name', 'selected_stage', 'selected_option', 'script', 'tool', 
#             'deployment_type', 'framework', 'hosting_platform', 'programming_language', 
#             'project_type', 'testing_needs', 'created_at', 'updated_at'
#         ]


# class GeneratedScriptSerializer(serializers.ModelSerializer):
#     project_detail = ProjectDetailSerializer(read_only=True)  # Reference to ProjectDetail

#     class Meta:
#         model = GeneratedScript
#         fields = ['id', 'project_detail', 'script_content', 'created_at', 'updated_at']

# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Script, Tool, ProjectDetail, PipelineStage
# from .models import MonitoringData

# # User Serializer
# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password']

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user

# # PipelineStage Serializer
# class PipelineStageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PipelineStage
#         fields = ['id', 'name']


# # Script Serializer
# class ScriptSerializer(serializers.ModelSerializer):
#     stage = PipelineStageSerializer(read_only=True)

#     class Meta:
#         model = Script
#         fields = ['id', 'title', 'description', 'script_content', 'category', 'stage']

#     def create(self, validated_data):
#         """Ensure that the script is saved with the appropriate pipeline stage."""
#         pipeline_stage = validated_data.pop('stage', None)
#         script = Script.objects.create(**validated_data)
#         if pipeline_stage:
#             script.stage = pipeline_stage
#             script.save()
#         return script


# # Tool Serializer
# class ToolSerializer(serializers.ModelSerializer):
#     stage = PipelineStageSerializer(read_only=True)

#     class Meta:
#         model = Tool
#         fields = ['id', 'name', 'description', 'url', 'stage']

#     def create(self, validated_data):
#         """Ensure that the tool is saved with the appropriate pipeline stage."""
#         pipeline_stage = validated_data.pop('stage', None)
#         tool = Tool.objects.create(**validated_data)
#         if pipeline_stage:
#             tool.stage = pipeline_stage
#             tool.save()
#         return tool


# # ProjectDetail Serializer
# class ProjectDetailSerializer(serializers.ModelSerializer):
#     selected_stage = PipelineStageSerializer(read_only=True)
#     script = ScriptSerializer(read_only=True)  # If you want to include the script in the response
#     tool = ToolSerializer(read_only=True)

#     class Meta:
#         model = ProjectDetail
#         fields = [
#             'id', 'project_name', 'selected_stage', 'selected_option', 'script', 'tool', 
#             'deployment_type', 'framework', 'hosting_platform', 'programming_language', 
#             'project_type', 'testing_needs', 'created_at', 'updated_at'
#         ]

#     def create(self, validated_data):
#         """Create a new project detail and ensure it's properly linked."""
#         selected_stage = validated_data.pop('selected_stage', None)
#         script = validated_data.pop('script', None)
#         tool = validated_data.pop('tool', None)
#         project_detail = ProjectDetail.objects.create(**validated_data)

#         if selected_stage:
#             project_detail.selected_stage = selected_stage
#             project_detail.save()

#         if script:
#             project_detail.script = script
#             project_detail.save()

#         if tool:
#             project_detail.tool = tool
#             project_detail.save()

#         return project_detail


# class MonitoringDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MonitoringData
#         fields = ['cpu_usage', 'memory_usage', 'disk_usage', 'network_usage', 'timestamp']  # Include the fields you need

from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, validate_email
from django.core.exceptions import ValidationError
from .models import Script, Tool, ProjectDetail, PipelineStage, MonitoringData

class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_confirm')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

class PipelineStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PipelineStage
        fields = ['id', 'name']

class ScriptSerializer(serializers.ModelSerializer):
    stage = PipelineStageSerializer(read_only=True)
    
    class Meta:
        model = Script
        fields = ['id', 'title', 'description', 'script_content', 'category', 'stage']
        extra_kwargs = {
            'script_content': {'required': True},
            'title': {'min_length': 3},
        }

class ToolSerializer(serializers.ModelSerializer):
    stage = PipelineStageSerializer(read_only=True)
    
    class Meta:
        model = Tool
        fields = ['id', 'name', 'description', 'url', 'stage']
        extra_kwargs = {
            'name': {'min_length': 3},
            'url': {'required': True},
        }

class ProjectDetailSerializer(serializers.ModelSerializer):
    selected_stage = PipelineStageSerializer(read_only=True)
    script = ScriptSerializer(read_only=True)
    tool = ToolSerializer(read_only=True)

    class Meta:
        model = ProjectDetail
        fields = [
            'id', 'project_name', 'selected_stage', 'selected_option', 'script', 'tool', 
            'deployment_type', 'framework', 'hosting_platform', 'programming_language', 
            'project_type', 'testing_needs', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'project_name': {'min_length': 3, 'required': True},
        }

class MonitoringDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringData
        fields = ['cpu_usage', 'memory_usage', 'disk_usage', 'network_usage', 'timestamp']
        read_only_fields = ['timestamp']