from django.db import models

class PipelineStage(models.Model):
    name = models.CharField(max_length=50, unique=True)  # E.g., "Development", "Testing"

    def __str__(self):
        return self.name


class Script(models.Model):
    title = models.CharField(max_length=255)  # Name of the script
    description = models.TextField()  # Description or content
    script = models.URLField(blank=True, null=True)  # Optional URL for script
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


class ProjectDetail(models.Model):
    project_name = models.CharField(max_length=255)  # Name of the project
    project_type = models.CharField(max_length=100, default='default_project_type')  # Type of the project (e.g., web app, mobile app)
    programming_language = models.CharField(max_length=100, default='default_language') # Programming language used
    framework = models.CharField(max_length=100, default='default_framework') # Framework used for development
    hosting_platform =  models.CharField(max_length=100, default='default_platform')  # Hosting platform (e.g., AWS, Heroku)
    deployment_type = models.CharField(max_length=100, default='default_value')  # Type of deployment (e.g., containerized, serverless)
    testing_needs = models.CharField(max_length=100, default='None')   # Testing requirements (e.g., unit testing, integration testing)
    
    selected_stage = models.ForeignKey(PipelineStage, on_delete=models.SET_NULL, null=True)  # Linking to PipelineStage
    selected_option = models.CharField(max_length=50, choices=[  # Option for Script or Tool
        ('scripts', 'Scripts'),
        ('tools', 'Tools'),
    ], default='scripts')
    
    # You may choose to store the actual script or tool used, or just the reference
    script = models.ForeignKey(Script, on_delete=models.SET_NULL, null=True, blank=True)  # Optional script
    tool = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True, blank=True)  # Optional tool
    
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the record is created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the record is last updated

    def __str__(self):
        return f'{self.project_name} - {self.selected_stage.name if self.selected_stage else "Unknown Stage"}'
