# Generated by Django 4.2.7 on 2023-12-12 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objective', '0004_remove_objective_kpis_kpi_objectives'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kpi',
            name='objectives',
        ),
        migrations.AddField(
            model_name='kpi',
            name='objectives',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='objective_kpis', to='objective.objective'),
        ),
    ]
