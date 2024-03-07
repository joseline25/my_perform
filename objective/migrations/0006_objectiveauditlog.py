# Generated by Django 4.2.7 on 2024-03-01 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('objective', '0005_operationalgoal_objective_operational_goal'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectiveAuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('changes', models.TextField()),
                ('objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objective.objective')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]