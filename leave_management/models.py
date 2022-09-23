from django.db import models
from users.models import User



# Create your models here.
leavetype_choise = (
    ("Sick","Sick"),
    ("Casual","Casual"),
    ("Emergency" ,"Emergency"),
    ("Half-day", "Half-day"),
    ("full-day", "full-day")
    )



class Leave(models.Model):
    user = models.ForeignKey(User,related_name="leave",on_delete = models.CASCADE)
    leave_type = models.CharField( max_length=60,default='test',null=True)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    startdate = models.DateField(verbose_name=('Start Date'),help_text='leave start date is on ..',null=True,blank=False)
    enddate = models.DateField(verbose_name=('End Date'),help_text='coming back on ...',null=True,blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True, related_name="Approved_by")
    leave_status = models.CharField(max_length=30, default='pending') #pending,approved,rejected
    on_delete = models.BooleanField(default=False)
     



class Paid_leave:
    def leave():
        return 1

    
	