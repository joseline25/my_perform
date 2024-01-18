# Generated by Django 4.2.7 on 2024-01-17 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('objective', '0008_alter_teamskill_skill_id_alter_teamskill_team_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objective.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='users',
            field=models.ManyToManyField(through='objective.UserTeam', to=settings.AUTH_USER_MODEL),
        ),
    ]