# Generated by Django 4.0.6 on 2022-07-29 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contactlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_name', models.CharField(max_length=50)),
                ('Last_name', models.CharField(blank=True, max_length=50)),
                ('mobile', models.CharField(max_length=50)),
                ('Email', models.CharField(max_length=60)),
                ('Message', models.TextField(max_length=500)),
            ],
        ),
    ]