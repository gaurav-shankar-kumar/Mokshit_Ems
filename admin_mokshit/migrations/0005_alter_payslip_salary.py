# Generated by Django 4.0.6 on 2022-09-06 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_mokshit', '0004_payslip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payslip',
            name='salary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='salary_structure', to='admin_mokshit.salary'),
        ),
    ]
