from django.contrib import admin
from . models import Worklog

# Register your models here.

@admin.register(Worklog)
class WorklogAdmin(admin.ModelAdmin):
    list_display = ['id','user','project','task','work_start', 'work_end','work_time','extra_time']