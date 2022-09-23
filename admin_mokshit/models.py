from django.db import models

from users.models import User
from projects.models import Project
# Create your models here.




class Salary(models.Model):
    user = models.ForeignKey(User,related_name = 'salary',on_delete=models.CASCADE)
    basic = models.FloatField(default = 0)
    hra = models.FloatField(default = 0)
    increament = models.FloatField(default = 0)
    deduction = models.FloatField(default = 0)
    apply_from = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    action_by = models.ForeignKey(User,related_name = 'salary_action_by',on_delete=models.SET_NULL,blank=True,null=True)


class PaySlip(models.Model):
    salary = models.ForeignKey(Salary, related_name = 'salary_structure',blank=True, null=True,on_delete=models.SET_NULL)
    user = models.ForeignKey(User,related_name = 'payslip',on_delete=models.CASCADE)
    month_year = models.DateField()
    basic = models.FloatField(default = 0)
    hra = models.FloatField(default = 0)
    increament = models.FloatField(default = 0)
    deduction = models.FloatField(default = 0)
    total = models.FloatField(default = 0)
    remarks = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    action_by = models.ForeignKey(User,related_name = 'payslip_action_by',on_delete=models.SET_NULL,blank=True,null=True)


class Contacts(models.Model):
    phone_no = models.CharField(max_length=15,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    landmark = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    zip = models.CharField(max_length=100,null=True,blank=True)
    embed_link = models.URLField(max_length=500,null=True,blank=True)
    twitter_link = models.URLField(null=True,blank=True)
    fb_link = models.URLField(null=True,blank=True)
    insta_link = models.URLField(null=True,blank=True)
    skype_link = models.URLField(null=True,blank=True)
    linkedin_link = models.URLField(null=True,blank=True)


class Site_Team(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    sort = models.IntegerField()
    is_active = models.BooleanField(default=True)

class Client(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    quotes = models.TextField()
    image = models.ImageField(upload_to = 'static/client',default='static/client/default.jpg',null=True,blank=True)

class Count(models.Model):
    happy_client = models.IntegerField()
    total_project = models.IntegerField()
    hours_support = models.IntegerField()
    hard_worker = models.IntegerField()

class Portfolio(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    img_title = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'static/portfolio',default='static/portfolio/default.jpg',null=True,blank=True)

