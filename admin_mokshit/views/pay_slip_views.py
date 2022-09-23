from multiprocessing import context
from django.urls import reverse
from django.shortcuts import render,get_object_or_404
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


@login_required(login_url='/login/')
def pay_slip(request,pk=None):
    today = datetime.today().date()
    max_date = today - relativedelta(months=1)
    context = {'today':today,'max_date':max_date}
    if pk is not None:
        selected_user = get_object_or_404(User,pk=pk)
    else:
        selected_user = request.user
    all_payslip = selected_user.payslip.all()
    if request.GET.get('month'):
        select_month = (request.GET.get('month')).split('-')
        all_payslip = all_payslip.filter(month_year__month = select_month[1], month_year__year = select_month[0])
    context['selected_user'] = selected_user
    context['all_payslip'] = all_payslip
    return render (request,'admin/all_payslip.html',context)

@login_required(login_url='/login/')
def pay_slip_details(request,pk=None,pay_slip_id=None):
    context ={}
    if pay_slip_id is not None:
        payslip = get_object_or_404(PaySlip, pk =pay_slip_id)
        context['payslip'] = payslip
        try:
            increament = payslip.basic * payslip.increament / 100 
        except:
            increament = 0
        total = payslip.basic + payslip.hra + increament
        context['total'] = total
        context['net_total'] = num2words(payslip.total)
    return render (request,'admin/get_payslip.html',context)