# Generated by Django 4.0.6 on 2022-08-01 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='holiday_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]