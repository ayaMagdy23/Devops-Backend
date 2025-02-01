from rest_framework import serializers
from .models import PipelineStage, Script, Tool, User  # Ensure User is imported

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Ensure password is stored securely"""
        user = User.objects.create_user(**validated_data)
        return user

class PipelineStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PipelineStage
        fields = '__all__'

class ScriptSerializer(serializers.ModelSerializer):
    stage = serializers.PrimaryKeyRelatedField(queryset=PipelineStage.objects.all())

    class Meta:
        model = Script
        fields = '__all__'

class ToolSerializer(serializers.ModelSerializer):
    stage = serializers.PrimaryKeyRelatedField(queryset=PipelineStage.objects.all())

    class Meta:
        model = Tool
        fields = '__all__'
