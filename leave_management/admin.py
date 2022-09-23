from django.contrib import admin

# Register your models here.
from .models import Leave



@admin.register(Leave)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','user','leave_type','startdate','enddate','approved_by', 'leave_status']

