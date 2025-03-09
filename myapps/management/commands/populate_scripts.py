# your_app/management/commands/populate_scripts.py

from django.core.management.base import BaseCommand
from myapps.models import PipelineStage, Script, ProjectDetail

class Command(BaseCommand):
    help = 'Populate all possible scripts for each pipeline stage based on project details'

    def handle(self, *args, **kwargs):
        # Define the possible values for each project detail
        project_types = ['Web', 'API', 'Mobile']
        languages = ['Python', 'JavaScript', 'Go']
        frameworks = ['React', 'Django', 'Flask', 'Node.js']
        hosting_platforms = ['AWS', 'Heroku', 'Vercel']
        deployment_types = ['Docker', 'Kubernetes', 'Cloud']

        # Get all available pipeline stages
        pipeline_stages = PipelineStage.objects.all()

        # Loop through all combinations and generate scripts
        for project_type in project_types:
            for language in languages:
                for framework in frameworks:
                    for hosting in hosting_platforms:
                        for deployment in deployment_types:
                            # Create ProjectDetail instance to hold the project details
                            project_detail = ProjectDetail(
                                project_name=f"{project_type} - {language} - {framework}",
                                project_type=project_type,
                                programming_language=language,
                                framework=framework,
                                hosting_platform=hosting,
                                deployment_type=deployment
                            )
                            project_detail.save()

                            # For each stage, create a script
                            for stage in pipeline_stages:
                                # Generate a script for the current combination of project details and pipeline stage
                                script_content = self.generate_script_content(project_detail, stage)

                                # Save the script in the database
                                Script.objects.create(
                                    title=f"{project_type} {language} {framework} - {stage.name} Script",
                                    description=f"Script for {stage.name} stage of {project_type} project with {language} and {framework}.",
                                    script_content=script_content,
                                    category=project_type,
                                    stage=stage
                                )

        self.stdout.write(self.style.SUCCESS('Successfully populated scripts for all project details and stages'))

    def generate_script_content(self, project_detail, stage):
        """
        Generate script content based on the project details and stage.
        This logic can be expanded depending on the stage and project type.
        """
        # Example: Generate a simple script based on project details
        script = f"# {project_detail.project_name} - {stage.name} Setup\n"
        script += f"echo 'Setting up {project_detail.project_name} for {stage.name}...'\n"
        
        if stage.name == "Development":
            script += "echo 'Installing dependencies...'\n"
            if project_detail.framework == "React":
                script += "npx create-react-app my-app\n"
            if project_detail.framework == "Django":
                script += "django-admin startproject myproject\n"
        
        if stage.name == "Testing":
            script += "echo 'Running tests...'\n"
            script += "npm run test\n"
        
        if stage.name == "Deployment":
            script += "echo 'Deploying to the hosting platform...'\n"
            if project_detail.hosting_platform == "AWS":
                script += "aws deploy --project ${project_detail.project_name} --region us-west-2\n"
            if project_detail.hosting_platform == "Vercel":
                script += "vercel deploy\n"
        
        return script
