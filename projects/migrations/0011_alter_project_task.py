# Generated by Django 4.0.6 on 2022-09-05 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_rename_delete_project_on_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='task',
            field=models.ManyToManyField(blank=True, null=True, related_name='task', to='projects.tasks'),
        ),
    ]