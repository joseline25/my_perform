# Generated by Django 4.2.7 on 2024-01-20 05:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('objective', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement_name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_name', models.CharField(max_length=300)),
                ('completion_time', models.IntegerField()),
                ('comment', models.TextField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(blank=True, null=True)),
                ('number', models.IntegerField(null=True)),
                ('answer', models.BooleanField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActionTool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('action_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='action.action')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tool_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objective.tool')),
            ],
        ),
        migrations.CreateModel(
            name='ActionSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('action_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='action.action')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('skill_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='objective.skill')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ActionAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('achievement_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='action.achievement')),
                ('action_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='action.action')),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='action',
            name='achievements',
            field=models.ManyToManyField(related_name='achievement_actions', through='action.ActionAchievement', to='action.achievement'),
        ),
        migrations.AddField(
            model_name='action',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='action',
            name='collaborators',
            field=models.ManyToManyField(blank=True, related_name='actions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='action',
            name='objective',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='objective.objective'),
        ),
        migrations.AddField(
            model_name='action',
            name='questions',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='related_actions', to='action.question'),
        ),
        migrations.AddField(
            model_name='action',
            name='skills',
            field=models.ManyToManyField(related_name='skill_actions', through='action.ActionSkill', to='objective.skill'),
        ),
        migrations.AddField(
            model_name='action',
            name='tools',
            field=models.ManyToManyField(related_name='tool_actions', through='action.ActionTool', to='objective.tool'),
        ),
    ]
