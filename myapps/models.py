# from django.db import models

# class PipelineStage(models.Model):
#     name = models.CharField(max_length=50, unique=True)  # E.g., "Development", "Testing"

#     def __str__(self):
#         return self.name


# class Script(models.Model):
#     title = models.CharField(max_length=255)  # Name of the script
#     description = models.TextField()  # Description of the script
#     script_content = models.TextField()  # Store the actual script content (code/commands as text)
#     created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp
#     category = models.CharField(max_length=100, blank=True, null=True)  # Optional category
    
#     # Linking Script to a Pipeline Stage
#     stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE, default=1)

#     def __str__(self):
#         return self.title


# class Tool(models.Model):
#     name = models.CharField(max_length=100)  # Tool name
#     description = models.TextField()  # Tool description
#     url = models.URLField(blank=True, null=True)  # URL (optional)
    
#     # Linking Tool to a Pipeline Stage
#     stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE, default=1)

#     def __str__(self):
#         return self.name


# class ProjectDetail(models.Model):
#     project_name = models.CharField(max_length=255)  # Name of the project
#     project_type = models.CharField(max_length=100, default='default_project_type')  # Type of the project (e.g., web app, mobile app)
#     programming_language = models.CharField(max_length=100, default='default_language')  # Programming language used
#     framework = models.CharField(max_length=100, default='default_framework')  # Framework used for development
#     hosting_platform = models.CharField(max_length=100, default='default_platform')  # Hosting platform (e.g., AWS, Heroku)
#     deployment_type = models.CharField(max_length=100, default='default_value')  # Type of deployment (e.g., containerized, serverless)
#     testing_needs = models.CharField(max_length=100, default='None')  # Testing requirements (e.g., unit testing, integration testing)
    
#     selected_stage = models.ForeignKey(PipelineStage, on_delete=models.SET_NULL, null=True)  # Linking to PipelineStage
#     selected_option = models.CharField(max_length=50, choices=[  # Option for Script or Tool
#         ('scripts', 'Scripts'),
#         ('tools', 'Tools'),
#     ], default='scripts')
    
#     # You may choose to store the actual script or tool used, or just the reference
#     script = models.ForeignKey(Script, on_delete=models.SET_NULL, null=True, blank=True)  # Optional script
#     tool = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True, blank=True)  # Optional tool
    
#     created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the record is created
#     updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the record is last updated

#     def __str__(self):
#         return f'{self.project_name} - {self.selected_stage.name if self.selected_stage else "Unknown Stage"}'

# from django.db import models

# class PipelineStage(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name


# class Script(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     script_content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     category = models.CharField(max_length=100, blank=True, null=True)
#     stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE, default=1)

#     def __str__(self):
#         return self.title


# class Tool(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     url = models.URLField(blank=True, null=True)
#     stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE, default=1)

#     def __str__(self):
#         return self.name


# class ProjectDetail(models.Model):
#     project_name = models.CharField(max_length=255)
#     project_type = models.CharField(max_length=100, default='default_project_type')
#     programming_language = models.CharField(max_length=100, default='default_language')
#     framework = models.CharField(max_length=100, default='default_framework')
#     hosting_platform = models.CharField(max_length=100, default='default_platform')
#     deployment_type = models.CharField(max_length=100, default='default_value')
#     testing_needs = models.CharField(max_length=100, default='None')

#     selected_stage = models.ForeignKey(PipelineStage, on_delete=models.SET_NULL, null=True)
#     selected_option = models.CharField(max_length=50, choices=[('scripts', 'Scripts'), ('tools', 'Tools')], default='scripts')

#     # Foreign keys to the generated script or tool
#     script = models.ForeignKey(Script, on_delete=models.SET_NULL, null=True, blank=True)
#     tool = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True, blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f'{self.project_name} - {self.selected_stage.name if self.selected_stage else "Unknown Stage"}'

#     def generate_script(self):
#         """
#         This method will generate a script for the project based on selected stage and option.
#         You can call OpenAI API or your logic here to generate scripts.
#         """
#         if self.selected_option == 'scripts' and self.selected_stage:
#             # Call OpenAI API or some logic to generate the script
#             generated_script = GeneratedScript.objects.create(
#                 project_detail=self,
#                 script_content="Generated script based on the selected stage and project details"
#             )
#             self.script = generated_script
#             self.save()
#             return generated_script
#         return None

#     def generate_tool(self):
#         """
#         This method can be used to generate or fetch the tools required for the selected stage.
#         """
#         if self.selected_option == 'tools' and self.selected_stage:
#             # Fetch tool(s) for the selected stage
#             # You can use logic to fetch a specific tool or predefined set
#             selected_tool = Tool.objects.filter(stage=self.selected_stage).first()  # Example logic
#             self.tool = selected_tool
#             self.save()
#             return selected_tool
#         return None


# class GeneratedScript(models.Model):
#     project_detail = models.ForeignKey(ProjectDetail, on_delete=models.CASCADE, related_name="generated_scripts")
#     script_content = models.TextField(default="Default script content")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f'Generated script for {self.project_detail.project_name}'

# 

from django.db import models

class PipelineStage(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Tool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)
    stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class ResourceFactory:
      """Factory Method to generate either a Script or a Tool dynamically."""

    @staticmethod
    def create_resource(resource_type, project_detail):
        if resource_type == "script":
            return Script.objects.create(
                stage=project_detail.selected_stage,
                title=f"{project_detail.project_name} Script",
                description="Auto-generated script",
                script_content="Generated script content"
            )
        elif resource_type == "tool":
            tool = Tool.objects.filter(stage=project_detail.selected_stage).first()
            return tool if tool else None
        else:
            raise ValueError("Invalid resource type specified")


class ProjectDetail(models.Model):
    project_name = models.CharField(max_length=255)
    project_type = models.CharField(max_length=100, default='default_project_type')
    programming_language = models.CharField(max_length=100, default='default_language')
    framework = models.CharField(max_length=100, default='default_framework')
    hosting_platform = models.CharField(max_length=100, default='default_platform')
    deployment_type = models.CharField(max_length=100, default='default_value')
    testing_needs = models.CharField(max_length=100, default='None')

    selected_stage = models.ForeignKey(PipelineStage, on_delete=models.SET_NULL, null=True)
    selected_option = models.CharField(
        max_length=50, choices=[('scripts', 'Scripts'), ('tools', 'Tools')], default='scripts'
    )

    script = models.ForeignKey(
        "Script", on_delete=models.SET_NULL, null=True, blank=True, related_name="project_details"
    )
    tool = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.project_name} - {self.selected_stage.name if self.selected_stage else "Unknown Stage"}'



    def generate_script(self):
     if self.selected_option == 'scripts' and self.selected_stage:
        script = ResourceFactory.create_resource("script", self)
        self.script = script
        self.save(update_fields=['script'])
        return script
     return None

    def generate_tool(self):
     if self.selected_option == 'tools' and self.selected_stage:
        tool = ResourceFactory.create_resource("tool", self)
        self.tool = tool
        self.save(update_fields=['tool'])
        return tool
     return None

class Script(models.Model):
    project_detail = models.ForeignKey(
        ProjectDetail, on_delete=models.CASCADE, related_name="scripts"
    )  
    stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    script_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title
    
    from django.db import models

class CloudInstance(models.Model):
    """
    Represents a cloud instance (e.g., AWS EC2, Azure VM) that needs monitoring.
    """
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=50, choices=[('AWS', 'AWS'), ('Azure', 'Azure'), ('GCP', 'GCP')])
    instance_id = models.CharField(max_length=100, unique=True)
    api_url = models.URLField(help_text="API endpoint for fetching instance metrics")

    def __str__(self):
        return f"{self.name} ({self.provider})"

class MonitoringData(models.Model):
    """
    Stores real-time monitoring data for each cloud instance.
    """
    instance = models.ForeignKey(CloudInstance, on_delete=models.CASCADE, related_name="monitoring_data")
    cpu_usage = models.FloatField(help_text="CPU usage in percentage")
    memory_usage = models.FloatField(help_text="Memory usage in percentage")
    network_usage = models.FloatField(help_text="Network usage in percentage")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Metrics for {self.instance.name} at {self.timestamp}"


class ScalingAction(models.Model):

    instance = models.ForeignKey(CloudInstance, on_delete=models.CASCADE, related_name="scaling_actions")
    action = models.CharField(max_length=50, choices=[("scale_up", "Scale Up"), ("scale_down", "Scale Down")])
    status = models.CharField(max_length=50, help_text="Status of scaling operation (e.g., Success, Failed)")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.instance.name} - {self.action} at {self.timestamp}"


class MonitoringData(models.Model):
    """
    Stores real-time monitoring data for each cloud instance.
    """
    instance = models.ForeignKey(CloudInstance, on_delete=models.CASCADE, related_name="monitoring_data")
    cpu_usage = models.FloatField(help_text="CPU usage in percentage")
    memory_usage = models.FloatField(help_text="RAM usage in percentage")
    network_usage = models.FloatField(help_text="Network usage in percentage")  # Fixed help text
    disk_usage = models.FloatField(help_text="Disk usage in percentage")  # Added missing field
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Metrics for {self.instance.name} at {self.timestamp}"


class ScalingAction(models.Model):
    """
    Tracks AI-driven scaling actions for cloud instances.
    """
    instance = models.ForeignKey(CloudInstance, on_delete=models.CASCADE, related_name="scaling_actions")
    action = models.CharField(max_length=50, choices=[("scale_up", "Scale Up"), ("scale_down", "Scale Down")])
    status = models.CharField(max_length=50, help_text="Status of scaling operation (e.g., Success, Failed)")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.instance.name} - {self.action} at {self.timestamp}"


