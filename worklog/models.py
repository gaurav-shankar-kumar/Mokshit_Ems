from pydoc import describe
from django.db import models
from users.models import User
from projects.models import Project, Tasks
# Create your models here.


class Worklog(models.Model):
    user = models.ForeignKey(User,related_name="worklog",on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks,on_delete=models.CASCADE)
    work_start = models.DateTimeField()
    work_end = models.DateTimeField()
    work_time = models.TimeField()
    extra_time = models.TimeField()
    active_time = models.TimeField(blank=True,null=True)
    describe = models.TextField(blank=True,null=True)
    delete = models.BooleanField(default=False)


