# Generated by Django 5.1.5 on 2025-02-09 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PipelineStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255)),
                ('project_type', models.CharField(default='default_project_type', max_length=100)),
                ('programming_language', models.CharField(default='default_language', max_length=100)),
                ('framework', models.CharField(default='default_framework', max_length=100)),
                ('hosting_platform', models.CharField(default='default_platform', max_length=100)),
                ('deployment_type', models.CharField(default='default_value', max_length=100)),
                ('testing_needs', models.CharField(default='None', max_length=100)),
                ('selected_option', models.CharField(choices=[('scripts', 'Scripts'), ('tools', 'Tools')], default='scripts', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('selected_stage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapps.pipelinestage')),
            ],
        ),
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('script_content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('project_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scripts', to='myapps.projectdetail')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapps.pipelinestage')),
            ],
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='script',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_details', to='myapps.script'),
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('url', models.URLField(blank=True, null=True)),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapps.pipelinestage')),
            ],
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='tool',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapps.tool'),
        ),
    ]
