from django.contrib import admin
from .models import Budget, Project, Tasks
# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id','title','client','created_at','updated_at', 'project_start']

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ['id','user','title','created_at','updated_at', 'assign_by']

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'estimeted_budget', 'total_amount']
