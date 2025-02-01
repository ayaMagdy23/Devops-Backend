from rest_framework import serializers
from .models import PipelineStage, Script, Tool

class PipelineStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PipelineStage
        fields = '__all__'  # Includes all fields

class ScriptSerializer(serializers.ModelSerializer):
    stage = serializers.PrimaryKeyRelatedField(queryset=PipelineStage.objects.all())

    class Meta:
        model = Script
        fields = '__all__'  # Includes all fields

    def validate_stage(self, value):
        """Ensure the provided stage exists"""
        if not PipelineStage.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Selected stage does not exist.")
        return value

class ToolSerializer(serializers.ModelSerializer):
    stage = serializers.PrimaryKeyRelatedField(queryset=PipelineStage.objects.all())

    class Meta:
        model = Tool
        fields = '__all__'  # Includes all fields

    def validate_stage(self, value):
        """Ensure the provided stage exists"""
        if not PipelineStage.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Selected stage does not exist.")
        return value
