# Generated by Django 4.0.6 on 2022-09-16 05:08

import birthday.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0045_alter_user_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=birthday.fields.BirthdayField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='tech',
            field=models.ManyToManyField(to='users.tech'),
        ),
    ]