# Generated by Django 4.2.7 on 2023-12-14 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('objective', '0006_rename_objectives_kpi_objective'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objective',
            name='assign_to',
            field=models.ManyToManyField(blank=True, null=True, related_name='objectives_assigned_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='objective',
            name='associated_task',
            field=models.ManyToManyField(blank=True, null=True, related_name='objectives', to='objective.task'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='dog',
            field=models.ManyToManyField(blank=True, null=True, related_name='definition_of_good', to='objective.definitionofgood'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='evaluator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='objective',
            name='skills',
            field=models.ManyToManyField(blank=True, null=True, related_name='objectives_skill', through='objective.ObjectiveSkill', to='objective.skill'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='tools',
            field=models.ManyToManyField(blank=True, null=True, related_name='objectives_tool', through='objective.ObjectiveTool', to='objective.tool'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='visible_to',
            field=models.ManyToManyField(blank=True, null=True, related_name='visible_objectives', to=settings.AUTH_USER_MODEL),
        ),
    ]
