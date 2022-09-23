from django.db import models


# Create your models here.
class Contactlist(models.Model):
    name = models.CharField(max_length=150,blank=True,null=True)
    subject = models.CharField(max_length=150,blank=True,null=True)
    Email = models.CharField(max_length=100,blank=True,null=True)
    Message = models.TextField(blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)