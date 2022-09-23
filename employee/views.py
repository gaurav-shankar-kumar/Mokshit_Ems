from django.contrib import messages
from django.shortcuts import render
from datetime import datetime
from users.models import User
# from .models import Task
from holidays.models import Holiday
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
from projects.models import Project,Tasks
from leave_management.models import Leave




# Create your views here.
@login_required(login_url='/login/')
def emppanel(request):
    selected_user = request.user
    today = datetime.now().date()
    last_month = today - relativedelta(months=1)
    all_users = User.objects.filter(is_active = True,is_superuser = False).order_by('-joining_date')
    all_projects = Project.objects.filter(on_delete = False).order_by('project_start')
    
    context = {'today' : today,'selected_user':selected_user}

    #Pending Task
    all_tasks = (Tasks.objects.filter(on_delete = False,user=selected_user) | Tasks.objects.filter(on_delete = False,assign_by=selected_user)).distinct()
    context['pending_task'] = all_tasks.filter(user_status = False)
    context['all_task'] = all_tasks
    try:
        task_ratio = all_tasks.filter(user_status = True).count() / all_tasks.count() * 100
    except:
        task_ratio = 0
    context['task_complete_ratio'] = task_ratio
    context['overdue_task'] = all_tasks.filter(due_date__lte = today,user_status = False)

    # Recenet Users
    context['recent_users'] =  all_users[:12]

    # Projects
    project_users = set()
    all_projects = (Project.objects.filter(on_delete = False,project_controll_by=selected_user,project_status = False).order_by('project_start') | Project.objects.filter(on_delete = False,project_assign=selected_user,project_status = False).order_by('project_start')).distinct()
    for project in all_projects :
        for id in  project.project_controll_by.values_list('id',flat=True):
            project_users.add(id)
        for id in  project.project_assign.values_list('id',flat=True):
            project_users.add(id)
    project_users = list(project_users)
    print(project_users)
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
    context['team_members'] = all_users.filter(id__in = project_users).exclude(id = selected_user.id)
    print(context['team_members']) 

    # leave & Holiday
    all_leaves = Leave.objects.filter(enddate__gte = today,user__in = project_users,leave_status='accept') # ,leave_status='accept'
    all_holiday = Holiday.objects.filter(is_deleted = False,holiday_date__gte = today)
    context['all_leaves'] = all_leaves
    context['upcoming_holiday'] = all_holiday
    print(all_leaves)
    

    #recent Birthdays
    context['recent_birthdays'] = User.empbday.get_upcoming_birthdays().filter(is_active = True,is_superuser = False)
    context['today_birthday'] = User.empbday.get_birthdays().filter(is_active = True,is_superuser = False,id = selected_user.id)
    context['leave_request'] = Leave.objects.filter(user = selected_user,enddate__gte = today).order_by('startdate')
    return render(request,'employee/emppanel.html',context)
