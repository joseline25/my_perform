# Generated by Django 4.2.7 on 2023-11-30 23:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Achievement',
            },
        ),
        migrations.CreateModel(
            name='DefinitionOfGood',
            fields=[
                ('dog_id', models.AutoField(primary_key=True, serialize=False)),
                ('dog_criteria', models.CharField(max_length=100)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Dog',
            },
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('objective_id', models.AutoField(primary_key=True, serialize=False)),
                ('objective_name', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('repeat_date', models.DateTimeField(blank=True, null=True)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('action_phrase', models.CharField(blank=True, max_length=300)),
                ('number', models.IntegerField()),
                ('units', models.CharField(max_length=10)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Intermediate', 'Intermediate'), ('High', 'High')], max_length=100)),
                ('complexity', models.CharField(choices=[('Easy', 'Easy'), ('Hard', 'Hard')], max_length=100)),
                ('objective_type', models.CharField(choices=[('Financial', 'Financial'), ('Non-Financial', 'Non-Financial')], max_length=100)),
                ('is_draft', models.BooleanField(default=False)),
                ('repeat', models.BooleanField(default=False)),
                ('assign_to', models.ManyToManyField(related_name='objectives_assigned_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('skill_id', models.AutoField(primary_key=True, serialize=False)),
                ('skill_name', models.CharField(max_length=100)),
                ('skill_description', models.TextField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(max_length=300)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TeamTool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objective.team')),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('tool_id', models.AutoField(primary_key=True, serialize=False)),
                ('tool_name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('teams', models.ManyToManyField(related_name='tools', through='objective.TeamTool', to='objective.team')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='teamtool',
            name='tool_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objective.tool'),
        ),
        migrations.AddField(
            model_name='teamtool',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='TeamSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('skill_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objective.skill')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objective.team')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.AddField(
            model_name='team',
            name='skills',
            field=models.ManyToManyField(related_name='skills', through='objective.TeamSkill', to='objective.skill'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('taskCode', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('summary', models.TextField(blank=True)),
                ('duration', models.DecimalField(decimal_places=3, max_digits=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Review', 'Review')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('achievement', models.ForeignKey(db_column='achievement', on_delete=django.db.models.deletion.CASCADE, to='objective.achievement')),
            ],
            options={
                'db_table': 'Task',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ObjectiveTool',
            fields=[
                ('objective_tool_id', models.AutoField(primary_key=True, serialize=False)),
                ('tool_name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('objective_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objective.objective')),
                ('tool_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objective.tool')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ObjectiveSkill',
            fields=[
                ('objective_skill_id', models.AutoField(primary_key=True, serialize=False)),
                ('skill_name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('objective_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objective.objective')),
                ('skill_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objective.skill')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='objective',
            name='associated_task',
            field=models.ManyToManyField(related_name='objectives', to='objective.task'),
        ),
        migrations.AddField(
            model_name='objective',
            name='dog',
            field=models.ManyToManyField(related_name='definition_of_good', to='objective.definitionofgood'),
        ),
        migrations.AddField(
            model_name='objective',
            name='evaluator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='objective',
            name='skills',
            field=models.ManyToManyField(related_name='objectives_skill', through='objective.ObjectiveSkill', to='objective.skill'),
        ),
        migrations.AddField(
            model_name='objective',
            name='tools',
            field=models.ManyToManyField(related_name='objectives_tool', through='objective.ObjectiveTool', to='objective.tool'),
        ),
        migrations.AddField(
            model_name='objective',
            name='visible_to',
            field=models.ManyToManyField(related_name='visible_objectives', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Collaboration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(db_column='task', on_delete=django.db.models.deletion.CASCADE, to='objective.task')),
            ],
            options={
                'db_table': 'Collaboration',
            },
        ),
    ]
