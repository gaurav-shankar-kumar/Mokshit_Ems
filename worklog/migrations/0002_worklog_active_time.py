# Generated by Django 4.0.6 on 2022-08-16 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worklog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='worklog',
            name='active_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]