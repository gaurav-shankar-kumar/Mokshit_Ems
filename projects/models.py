from django.db import models
from users.models import User

# Create your models here.

class Tasks(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User,related_name='all_task',on_delete = models.SET_NULL,blank=True,null=True)
    user_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(blank=True, null=True)
    assign_by = models.ForeignKey(User, related_name='task_assign_by',on_delete = models.SET_NULL,blank=True,null=True)
    completed = models.BooleanField(default=False)
    on_delete = models.BooleanField(default=False)
    

class Project(models.Model):
    title = models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    task = models.ManyToManyField(Tasks, related_name='project')
    client = models.CharField(max_length=200,blank=True,null=True)
    project_assign = models.ManyToManyField(User,related_name='project_assign')
    project_controll_by = models.ManyToManyField(User, related_name='project_controll_by')
    project_status = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created_by = models.ForeignKey(User,related_name='project_created_by',on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    project_start = models.DateTimeField(blank=True,null=True)
    project_end = models.DateTimeField(blank=True,null=True)
    on_delete = models.BooleanField(default=False)


class Budget(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    estimeted_budget = models.IntegerField()
    total_amount = models.IntegerField()