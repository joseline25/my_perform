# Generated by Django 4.2.7 on 2024-02-27 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0003_actionmainentry_collaborators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionmainentry',
            name='achievements',
            field=models.CharField(choices=[('Learnings', 'Learnings'), ('Deliverable', 'Deliverable'), ('Work-Product', 'Work-Product'), ('Innovation', 'Innovation'), ('Miscellaneous', 'Miscellaneous')], default='Learnings', max_length=20),
        ),
    ]