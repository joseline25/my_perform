# Generated by Django 3.2.9 on 2024-01-18 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objective', '0010_alter_objective_repeat_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objective',
            name='repeat_date',
            field=models.CharField(blank=True, choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')], max_length=100, null=True),
        ),
    ]
