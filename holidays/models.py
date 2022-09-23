from django.db import models
from users.models import User

import datetime

# # Create your models here.


class Holiday(models.Model):
    
    holidayname = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    holiday_date = models.DateField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True, related_name="created_by")

    
    
