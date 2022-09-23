from django.contrib import admin

from .models import Holiday

# Register your models here.

@admin.register(Holiday)
class Holiday(admin.ModelAdmin):
    list_display = ['id','holidayname','created_at', 'holiday_date',]


