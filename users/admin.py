from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','first_name','last_name','is_staff']
 


@admin.register(User_Group)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['id','group_name']

@admin.register(Bank_Details)
class Bank_DetailsAdmin(admin.ModelAdmin):
    list_display = ['user','bank_name','ac_no']

@admin.register(Tech)
class TechAdmin(admin.ModelAdmin):
    list_display = ['id','tech_name']
