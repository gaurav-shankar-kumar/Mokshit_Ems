# Generated by Django 4.0.5 on 2022-07-22 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leave_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Approved_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
