# Generated by Django 4.2.7 on 2024-02-28 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objective', '0003_kpi_frequency_alter_objective_complexity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='objective',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
