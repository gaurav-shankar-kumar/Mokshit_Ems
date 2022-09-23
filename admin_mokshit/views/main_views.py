from datetime import datetime
from django.urls import reverse
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from users.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from projects.models import Project,Tasks,Budget
from leave_management.models import Leave
from holidays.models import Holiday
from . . models import Salary
from . session_users import get_all_logged_in_users
from dateutil.relativedelta import relativedelta
from .. permissions import administration_permission_required


# # Create your views here.
@administration_permission_required()
def admindashboard(request):
    today = datetime.now().date()
    last_month = today - relativedelta(months=1)
    all_users = User.objects.filter(is_active = True,is_superuser = False).order_by('-joining_date')
    all_projects = Project.objects.filter(on_delete = False).order_by('project_start')
    all_tasks = Tasks.objects.filter(on_delete = False)
    all_leave = Leave.objects.filter(startdate__gte = today)
    all_holiday = Holiday.objects.filter(is_deleted = False,holiday_date__gte = today)
    login_users = get_all_logged_in_users()
    context = {'today' : today,'all_users':all_users}

    #Pending Task
    context['pending_task'] = all_tasks.filter(user_status=False)
    context['today_leave'] = all_leave.filter(startdate = today,leave_status = 'accept')
    context['login_users'] = login_users

    # Recenet Users
    context['recent_users'] =  all_users[:12]

    # Recent Projects
    recent_project_data = []
    for project in all_projects[:10]:
        total_task = project.task
        complete_task = project.task.filter(user_status=True)
        try:
            percent = complete_task.count()/total_task.count() * 100
        except:
            percent = 0

        recent_project_data.append({'project':project,'total_task':total_task,'complete_task':complete_task,'percent':percent})
    context['recent_projects'] = recent_project_data

    #recent Birthdays
    context['recent_birthdays'] = User.empbday.get_upcoming_birthdays().filter(is_active = True,is_superuser = False)
    context['today_birthday'] = User.empbday.get_birthdays().filter(is_active = True,is_superuser = False)

    # recent Tasks
    context['recent_tasks'] = all_tasks.order_by('-created_at')[:12]

    # leave requests
    context['leave_request'] = all_leave.filter(leave_status='pending').order_by('startdate')
    context['all_leaves'] = Leave.objects.filter(leave_status='accept').order_by('startdate')

    # upcoming holidays
    context['upcoming_holiday'] = all_holiday.order_by('holiday_date')[:10]
    
    # salary Pending
    pending_salary_id = []
    for user in all_users:
        if user.salary.exists():
            salary = user.salary.filter().last()
            payslip = user.payslip.filter(month_year__year=last_month.year,month_year__month = last_month.month).first()
            if payslip is None:
                pending_salary_id.append(salary.id)
    salary_pending = Salary.objects.filter(id__in = pending_salary_id)
    context['pending_salary'] = salary_pending
    return render (request,'admin/admindashboard.html',context) 

    
def page_not_found_view(request, exception=None):
    return render(request, 'common/404.html', status=404)

def server_error(request, exception=None):
    return render(request, 'common/500.html', status=500)







    
# # function  for delete the User 
# @login_required(login_url='/login/')
# def Delete_user(request, id):
#     if request.method == 'POST':
#         del_user = User.objects.get(pk=id)
#         del_user.delete()
#         # return HttpResponseRedirect ('/allusers/')
#         return HttpResponseRedirect(reverse('all_users'))

        





