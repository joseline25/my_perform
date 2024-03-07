# Generated by Django 4.2.7 on 2024-03-07 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0007_alter_actionmainentry_options_action_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionmainentry',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Validated', 'Validated'), ('Rejected', 'Rejected')], default='Pending', max_length=300),
        ),
    ]