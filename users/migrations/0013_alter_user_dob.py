# Generated by Django 4.0.6 on 2022-08-01 10:24

import birthday.fields
import datetime
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_user_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=birthday.fields.BirthdayField(blank=True, default=datetime.datetime(2022, 8, 1, 15, 54, 25, 58594)),
        ),
    ]
