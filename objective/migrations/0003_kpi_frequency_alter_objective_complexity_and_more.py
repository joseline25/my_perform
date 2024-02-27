# Generated by Django 4.2.7 on 2024-02-27 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objective', '0002_objective_completion_date_objective_estimated_hours_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpi',
            name='frequency',
            field=models.CharField(choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')], default='Daily', max_length=300),
        ),
        migrations.AlterField(
            model_name='objective',
            name='complexity',
            field=models.CharField(choices=[('Easy', 'Easy'), ('Hard', 'Hard')], max_length=300),
        ),
        migrations.AlterField(
            model_name='objective',
            name='objective_type',
            field=models.CharField(choices=[('Financial', 'Financial'), ('Non-Financial', 'Non-Financial')], max_length=300),
        ),
        migrations.AlterField(
            model_name='objective',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Intermediate', 'Intermediate'), ('High', 'High')], max_length=300),
        ),
        migrations.AlterField(
            model_name='objective',
            name='repeat_date',
            field=models.CharField(blank=True, choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')], max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='objective',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending', max_length=300),
        ),
        migrations.AlterField(
            model_name='objective',
            name='units',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='skill',
            name='skill_name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='tool',
            name='description',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='tool',
            name='tool_name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
