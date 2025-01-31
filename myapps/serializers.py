from rest_framework import serializers
from .models import PipelineStage, Script, Tool

class PipelineStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PipelineStage
        fields = '__all__'  # Includes all fields

class ScriptSerializer(serializers.ModelSerializer):
    stage = serializers.SlugRelatedField(slug_field='name', queryset=PipelineStage.objects.all())
    
    class Meta:
        model = Script
        fields = '__all__'  # Includes all fields

class ToolSerializer(serializers.ModelSerializer):
    stage = serializers.SlugRelatedField(slug_field='name', queryset=PipelineStage.objects.all())
    
    class Meta:
        model = Tool
        fields = '__all__'  # Includes all fields
