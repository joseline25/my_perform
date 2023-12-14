# Generated by Django 4.2.7 on 2023-12-14 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('objective', '0007_alter_objective_assign_to_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamskill',
            name='skill_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='objective.skill'),
        ),
        migrations.AlterField(
            model_name='teamskill',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='objective.team'),
        ),
        migrations.AlterField(
            model_name='teamskill',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teamtool',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='objective.team'),
        ),
        migrations.AlterField(
            model_name='teamtool',
            name='tool_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='objective.tool'),
        ),
        migrations.AlterField(
            model_name='teamtool',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
