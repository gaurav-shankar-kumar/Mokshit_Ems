from django.contrib import messages
from django.shortcuts import render, redirect
import datetime
from django.contrib.auth.decorators import login_required

from .models import Holiday
from admin_mokshit.permissions import administration_permission_required
# Create your views here.

@administration_permission_required()
def add_holiday(request):
    # print('hello')
    if request.method == "POST":
        Holiday_Name = request.POST['name']
        HolidayDate = request.POST['h-date']
        # print(request.POST['date'],'helo')
        
        holidays = Holiday(created_by=request.user,holidayname=Holiday_Name,holiday_date=HolidayDate)
        holidays.save()
        messages.success(request,f'Holiday {Holiday_Name} Added Sucessfully!')
        return redirect ('all_holiday')
    return render(request,'admin/addholiday.html')


@login_required(login_url='/login/')
def all_holidays(request):
    today = datetime.datetime.now().date()
    all_holiday = Holiday.objects.filter(is_deleted = False).order_by('holiday_date')
    upcoming_holiday = all_holiday.filter(holiday_date__gte=datetime.datetime.now()).order_by('holiday_date')
    context = {'today':today,'all_holiday':all_holiday,'upcoming_holiday':upcoming_holiday}
    return render(request,'common/allholiday.html',context)