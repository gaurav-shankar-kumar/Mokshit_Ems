import time
from django.urls import reverse
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from ..models import Salary,PaySlip
from users.models import User
from holidays.models import Holiday
from datetime import datetime,date,timedelta
import calendar
from leave_management.models import Paid_leave
import numpy as np
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from num2words import num2words
from dateutil.relativedelta import relativedelta
from .. permissions import administration_permission_required

@administration_permission_required()
def salary_management(request):
    context = {}
    today = datetime.today().date()
    max_date = today - relativedelta(months=1)
    current_date = max_date

    context['today'] = today
    context['max_date'] = current_date
    if request.GET.get('month') :
        select_month = (request.GET.get('month')).split('-')
        current_date = datetime(int(select_month[0]), int(select_month[1]), 1).date()
        print('ok')
        if current_date > max_date:
            messages.error(request,f"Don't be Over-Smart, If you are Bad I am Your Dad! 🤣 Select Month properly!")
            current_date = max_date
    context['current_date'] = current_date
    current_month_s_date = current_date.replace(day=1)
    current_month_e_date = current_date.replace(day = calendar.monthrange(current_date.year, current_date.month)[1])
    total_working_day = np.busday_count(current_month_s_date,(current_month_e_date + timedelta(days=1)))
    # print(total_working_day)
    
    all_users = User.objects.filter(is_active=True).order_by('first_name')
    if request.GET.get('search'):
        search_query = request.GET.get('search')
        all_users = all_users.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) | Q(email__icontains=search_query) | Q(role__icontains=search_query))
        context['search_query'] = search_query
    delta = current_month_e_date - current_month_s_date  # as timedelta
    days = [current_month_s_date + timedelta(days=i) for i in range(delta.days + 1)]
    working_date = []
    for d in days:
        if d.strftime("%A") == 'Saturday' or d.strftime("%A") == 'Sunday':
            pass
        else:
            working_date.append(d)
    print(working_date)
    datas = []
    for user in all_users:

        # Holiday datas
        total_holiday = 0
        for i in working_date:
            if Holiday.objects.filter(holiday_date = i).exists():
                total_holiday += 1
        data3 = {'total_holiday':total_holiday}
        
        # Worklog in a day
        total_work_on_month = 0
        for one_day in days:
            if user.worklog.filter(work_start__date = one_day).exists():
                total_work_on_month += 1
        exact_work_day = total_working_day-total_holiday
        data1= {'working_days':total_work_on_month,'total_bussines_day':total_work_on_month,'total_working_day':exact_work_day}

        # Leave Data
        leave_data = user.leave.filter(on_delete=False,leave_status='accept').filter(startdate__lte=current_month_e_date,enddate__gte = current_month_s_date)
        total_leave_month = 0
        if leave_data is not None:
            for l in leave_data:
                if l.enddate > current_month_e_date:
                    total_leave_month += np.busday_count((l.startdate),(current_month_e_date + timedelta(days=1)))
                    print('--------------',l.enddate,(current_month_e_date-l.startdate + timedelta(days=1)))
                    ds = np.busday_count((l.startdate),(current_month_e_date + timedelta(days=1)))
                    print('Number of business days is:', type(ds))
                elif l.startdate < current_month_s_date:
                    total_leave_month += np.busday_count((current_month_s_date),(l.enddate + timedelta(days=1)))
                    print(l.startdate,'--------------',(l.enddate - current_month_s_date + timedelta(days=1)))
                    ds = np.busday_count((current_month_s_date),(l.enddate + timedelta(days=1)))
                    print('Number of business days is:', ds)
                else :
                    total_leave_month += np.busday_count((l.startdate ),(l.enddate + timedelta(days=1)))
                    print('      --------------',(l.enddate - l.startdate + timedelta(days=1))) 
                    ds = np.busday_count((l.startdate ),(l.enddate + timedelta(days=1)))
                    print('Number of business days is:', ds)
        data2 = {'leave_days':total_leave_month,}    
        
        
        

        # salaray Datas
        salary_data = user.salary.filter(apply_from__lte = current_month_s_date).last()
        payslip = user.payslip.filter(month_year__year=current_date.year,month_year__month = current_date.month).first()
        deduction = 0
        basic,hra,increament,basic_increament = 0,0,0,0
        if salary_data is not None:
            basic,hra,deduction,increament = salary_data.basic,salary_data.hra,salary_data.deduction+deduction,salary_data.increament
            if increament != 0:basic_increament = (basic/increament*100)
            if basic != 0:
                deduction = (basic/exact_work_day)*(exact_work_day-total_work_on_month)
        
        total = (basic + hra + basic_increament - deduction)
        data5 = {'salary_data': salary_data,'payslip':payslip,'basic': basic,'hra': hra,'increament': increament,'deduction': deduction,'total': total}
        datas.append({'user':user,'work_data':data1,'leave_data':data2,'holiday_data':data3,'salary_data':data5})
    if request.POST:
        print(request.POST)
        _user = all_users.get(id = int(request.POST.get('user-id')))
        if request.POST.get('salary_structure_id'):
            salary_structure = Salary.objects.get(id = int(request.POST.get('salary_structure_id')))
        _basic = float(request.POST.get('basic'))
        _hra = float(request.POST.get('hra'))
        _increament = float(request.POST.get('increament'))
        _deduction = float(request.POST.get('deduction'))
        _total = float(request.POST.get('total'))
        _remarks = request.POST.get('remarks')
        if PaySlip.objects.filter(user = _user,month_year__year=current_date.year,month_year__month = current_date.month).exists():
            print('ok')
        else:
            payslip = PaySlip.objects.create(user = _user, month_year = current_date, basic = _basic, hra = _hra, increament = _increament, deduction = _deduction, total = _total, remarks = _remarks, action_by = request.user)
            payslip
            if request.POST.get('salary_structure_id'):
                salary_structure = Salary.objects.get(id = int(request.POST.get('salary_structure_id')))
                payslip.salary = salary_structure
                payslip.save()
            messages.success(request,f'PaySlip no.{payslip.id} is Generated for {_user.get_full_name()}')
            return salary_management(request)

        # if user QueryDict: {'csrfmiddlewaretoken': ['V2tSSDlBP6dapWnGN3DHQGKBk7FL9xuYTx7F9dTmox0bX0mjIhDJMfSwvltgDrfv'], 'basic': ['5000.0'], 'hra': ['2000.0'], '': ['0.0'], '': ['4250.0'], '': ['2750.0'], '': ['']}
        pass
    context['datas'] = datas
    return render(request,'admin/salary_management.html',context)




def user_salary(user=None):
    context = {}
    today = datetime.today().date()
    # if request.GET.get('month'):
    #     select_month = (request.GET.get('month')).split('-')
    #     today = datetime(int(select_month[0]), int(select_month[1]), 1).date()
    current_date = today
    context['current_date'] = current_date
    current_month_s_date = current_date.replace(day=1)
    current_month_e_date = current_date.replace(day = calendar.monthrange(current_date.year, current_date.month)[1])
    total_working_day = np.busday_count(current_month_s_date,(current_month_e_date + timedelta(days=1)))
    # print(total_working_day)
    
    delta = current_month_e_date - current_month_s_date  # as timedelta
    days = [current_month_s_date + timedelta(days=i) for i in range(delta.days + 1)]
    working_date = []
    for d in days:
        if d.strftime("%A") == 'Saturday' or d.strftime("%A") == 'Sunday':
            pass
        else:
            working_date.append(d)
    print(working_date)
    if user is not None:

        # Holiday datas
        total_holiday = 0
        for i in working_date:
            if Holiday.objects.filter(holiday_date = i).exists():
                total_holiday += 1
        data3 = {'total_holiday':total_holiday}
        
        # Worklog in a day
        total_work_on_month = 0
        for one_day in days:
            if user.worklog.filter(work_start__date = one_day).exists():
                total_work_on_month += 1
        exact_work_day = total_working_day-total_holiday
        data1= {'working_days':total_work_on_month,'total_bussines_day':total_work_on_month,'total_working_day':exact_work_day}

        # Leave Data
        leave_data = user.leave.filter(on_delete=False,leave_status='accept').filter(startdate__lte=current_month_e_date,enddate__gte = current_month_s_date)
        total_leave_month = 0
        if leave_data is not None:
            for l in leave_data:
                if l.enddate > current_month_e_date:
                    total_leave_month += np.busday_count((l.startdate),(current_month_e_date + timedelta(days=1)))
                    print('--------------',l.enddate,(current_month_e_date-l.startdate + timedelta(days=1)))
                    ds = np.busday_count((l.startdate),(current_month_e_date + timedelta(days=1)))
                    print('Number of business days is:', type(ds))
                elif l.startdate < current_month_s_date:
                    total_leave_month += np.busday_count((current_month_s_date),(l.enddate + timedelta(days=1)))
                    print(l.startdate,'--------------',(l.enddate - current_month_s_date + timedelta(days=1)))
                    ds = np.busday_count((current_month_s_date),(l.enddate + timedelta(days=1)))
                    print('Number of business days is:', ds)
                else :
                    total_leave_month += np.busday_count((l.startdate ),(l.enddate + timedelta(days=1)))
                    print('      --------------',(l.enddate - l.startdate + timedelta(days=1)))
                    ds = np.busday_count((l.startdate ),(l.enddate + timedelta(days=1)))
                    print('Number of business days is:', ds)
        data2 = {'leave_days':total_leave_month,}    
        
        
        

        # salaray Datas
        salary_data = user.salary.filter(apply_from__lte = current_month_s_date).last()
        payslip = user.payslip.all().order_by('-month_year')[:12]
        deduction = 0
        basic,hra,increament,basic_increament = 0,0,0,0
        if salary_data is not None:
            basic,hra,deduction,increament = salary_data.basic,salary_data.hra,salary_data.deduction+deduction,salary_data.increament
            if increament != 0:basic_increament = (basic/increament*100)
            if basic != 0:
                deduction = (basic/exact_work_day)*(exact_work_day-total_work_on_month)
        total = (basic + hra + basic_increament - deduction)
        total_earnings = basic + hra + basic_increament
        yearly = (basic + hra + basic_increament)*12
        data5 = {'salary_data':salary_data,'payslip':payslip,'basic':basic,'hra':hra,'increament':increament,'deduction':deduction,'total':total,'total_earnings':total_earnings,'yearly':yearly,'yearly_in_words':num2words(yearly)}
    return {'current_date':current_date,'user':user,'work_data':data1,'leave_data':data2,'holiday_data':data3,'salary_data':data5}

