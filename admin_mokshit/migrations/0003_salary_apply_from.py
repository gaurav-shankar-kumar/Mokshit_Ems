# Generated by Django 4.0.6 on 2022-08-30 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_mokshit', '0002_alter_salary_basic_alter_salary_deduction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='apply_from',
            field=models.DateField(blank=True, null=True),
        ),
    ]
