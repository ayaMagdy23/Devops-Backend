from django.db import models

class PipelineStage(models.Model):
    name = models.CharField(max_length=50, unique=True)  # E.g., "Development", "Testing"

    def __str__(self):
        return self.name

class Script(models.Model):
    title = models.CharField(max_length=255)  # Name of the script
    description = models.TextField()  # Description or content
    script_link = models.URLField(max_length=200, blank=True, null=True)  # Optional URL
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp
    category = models.CharField(max_length=100, blank=True, null=True)  # Optional category
    
    # Linking Script to a Pipeline Stage
    stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE, default=1) 

    def __str__(self):
        return self.title

class Tool(models.Model):
    name = models.CharField(max_length=100)  # Tool name
    description = models.TextField()  # Tool description
    url = models.URLField(blank=True, null=True)  # URL (optional)
    
    # Linking Tool to a Pipeline Stage
    stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE, default=1) 

    def __str__(self):
        return self.name
