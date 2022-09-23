from django.contrib import admin
from .models import Salary,PaySlip,Contacts,Site_Team,Client,Count,Portfolio
# Register your models here.
# from models import Salary

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['id','user','basic','hra','increament', 'deduction']

@admin.register(PaySlip)
class PaySlipAdmin(admin.ModelAdmin):
    list_display = ['id','user','basic','hra','increament', 'deduction']

admin.site.register(Contacts)


admin.site.register(Client)


admin.site.register(Count)


admin.site.register(Portfolio)

@admin.register(Site_Team)
class Site_TeamAdmin(admin.ModelAdmin):
    list_display = ['user','title','sort','is_active']
