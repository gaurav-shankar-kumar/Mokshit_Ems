import re
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import  datetime, timedelta,date,time

from users.models import User
from .models import Worklog
from projects.models import Tasks , Project
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/login/')
def worklog(request):
    all_users = User.objects.filter()
    context = {'all_users' : all_users}
    selected_user = request.user
    if request.GET.get('selected_user_id'):
        selected_user = all_users.get(id = int(request.GET.get('selected_user_id')))
    context['selected_user'] = selected_user
    today = datetime.now().date()
    e_day = today + timedelta(days=8)
    days = [today + timedelta(days=x) for x in range((e_day-today).days + 1) if (today + timedelta(days=x)).weekday() == 6]
    day_7th = days[0]
    
    # if request.GET.get('date'):
    #     day_7th = datetime.strptime(request.GET.get('date'), '%d/%m/%Y')
    if request.GET.get('week'):
        day_7th = datetime.strptime(request.GET.get('week') + '-0', "%Y-W%W-%w")
    day_6th = day_7th - timedelta(days=1)
    day_5th = day_6th - timedelta(days=1)
    day_4th = day_5th - timedelta(days=1)
    day_3th = day_4th - timedelta(days=1)
    day_2th = day_3th - timedelta(days=1)
    day_1th = day_2th - timedelta(days=1)
    days = [day_1th,day_2th,day_3th,day_4th,day_5th,day_6th,day_7th]
    workflow = []
    works = Worklog.objects.all()
    project = Project.objects.filter(project_status = False,project_assign = selected_user).filter(task__user_status=False,task__on_delete=False).distinct()
    # project = selected_user.all_task.all()
    # project = selected_user.all_task.filter(user_status =False,on_delete=False)
    for p in project:print(p)
    context['projects'] = project
    def time_to_string(obj):
        obj_time = (str(obj)).split(':')
        return f'{obj_time[0]}.{obj_time[1]}'
    for day in days:
        work_obj = works.filter(work_start__date = day,user = selected_user)
        zero_time = time(0, 0)
        work_time = time(8, 30)
        zero_time, extra_time = datetime.combine(date.min, zero_time) - datetime.min , datetime.combine(date.min, zero_time) - datetime.min
        work_time = datetime.combine(date.min, work_time) - datetime.min
        if work_obj is not None:
            print('46',work_obj)
            for w_obj in work_obj:zero_time += datetime.combine(date.min, w_obj.active_time) - datetime.min
            print('48',zero_time)
            if zero_time > work_time:
                extra_time = zero_time - work_time
            else:
                work_time = zero_time
        workflow.append({'day':day,'work_time':time_to_string(work_time),'extra_time':time_to_string(extra_time),'active_time':time_to_string(zero_time),'work_obj':work_obj,'worklog':{'work_time':work_time,'extra_time':extra_time,'active_time':zero_time}})
    context['workflow'] = workflow
    context['previous_week'] = day_7th - timedelta(days=7)
    context['current_date'] = day_7th
    context['next_week'] = day_7th + timedelta(days=7)
    if request.POST:
        if request.POST.get('project_task'):
            # context['open_modal'] = True
            project_task = request.POST.get('project_task').split(',')
            print(project_task)
            # selected_project_id = int(request.POST.get('project'))
            selected_project = project.get(id=int(project_task[0]))
            task_obj = selected_project.task.get(id=int(project_task[1]))
            context['selected_task'] = task_obj
        
        if request.POST.get('start_work'):
            context['selected_start_work'] = request.POST.get('start_work')
        if request.POST.get('end_work'):
            context['selected_end_work'] = request.POST.get('end_work')
        if request.POST.get('desc'):
            context['selected_desc'] = request.POST.get('desc')
        if request.POST.get('task_status') == 'yes':
            context['selected_task_status'] = True
        if request.POST.get('project_task')  and request.POST.get('start_work') and request.POST.get('end_work') and request.POST.get('desc'):
            start_work = datetime.fromisoformat(request.POST.get('start_work')).strftime('%Y-%m-%d %H:%M:%S')
            end_work = datetime.fromisoformat(request.POST.get('end_work')).strftime('%Y-%m-%d %H:%M:%S')
            desc = request.POST.get('desc')
            if datetime.strptime(end_work, '%Y-%m-%d %H:%M:%S') > datetime.strptime(start_work, '%Y-%m-%d %H:%M:%S'):
                total_work_time = (datetime.strptime(end_work, '%Y-%m-%d %H:%M:%S') - datetime.strptime(start_work, '%Y-%m-%d %H:%M:%S'))
                decided_work_time = time(8, 30)  #datetime.strptime('08:30', '%H:%M').time()
                decided_work_time = datetime.combine(date.min, decided_work_time) - datetime.min
                total_decided_work_time = time(23,59)
                total_decided_work_time = datetime.combine(date.min, total_decided_work_time) - datetime.min
                if total_work_time > decided_work_time:
                    work_time = '08:30'
                    extra_time = str(total_work_time-decided_work_time)
                    error = time(23, 59)  #datetime.strptime('08:30', '%H:%M').time()
                    error = datetime.combine(date.min, error) - datetime.min
                    if total_work_time > error:
                        messages.error(request,f"Working Time is Too Much, Please Contact To HR!")
                        context['open_modal'] = True
                        return render (request,'common/worklog/worklog.html', context)
                else:
                    work_time = str(total_work_time)
                    extra_time = '00:00'
                if Worklog.objects.filter(user=request.user,work_start__date=datetime.strptime(start_work, '%Y-%m-%d %H:%M:%S').date(),task=task_obj).exists():
                    messages.warning(request,f"Worklog Already Exists for {task_obj.title}")
                    context['open_modal'] = True
                else:
                    w_objs = Worklog.objects.filter(user=request.user,work_start__date=datetime.strptime(start_work, '%Y-%m-%d %H:%M:%S').date())
                    # zero_time = time(0, 0)
                    # zero_time = datetime.combine(date.min, zero_time) - datetime.min
                    zero_time = total_work_time
                    for w_obj in w_objs:zero_time += datetime.combine(date.min, w_obj.active_time) - datetime.min
                    print('zero_time',zero_time)
                    print('total_decided_work_time',total_decided_work_time)
                    if zero_time > total_decided_work_time:
                        messages.error(request,f"Your Total Work Time for Today is Exceed, Please Contact To HR!")
                        context['open_modal'] = True
                        return render (request,'common/worklog/worklog.html', context)
                    else :
                        worklog = Worklog(
                            user = selected_user,
                            project=selected_project,
                            task=task_obj,
                            work_start=start_work,
                            work_end=end_work,
                            work_time=work_time,
                            extra_time=extra_time,
                            active_time = str(total_work_time),
                            describe=desc
                            )
                        if request.POST.get('task_status'):
                            request.POST.get('task_status') == 'yes'
                            task_obj.user_status = True
                            task_obj.save()
                        worklog.save()
                        messages.success(request,f"New Work Log is Added for You!")
                        context['open_modal'] = False
                        return redirect ('worklog')
            else:
                messages.warning(request,f"Work End Time Must Be Greater Than Work Start Time")
                context['open_modal'] = True
    return render (request,'common/worklog/worklog.html', context)

# def create_worklog(request):
#     print(request.POST)
#     context = {}
#     projects = Project.objects.filter(project_assign = request.user,on_delete=False,project_status=False)
#     if request.POST.get('project'):
#         project_id = int(request.POST.get('project'))
#         project = projects.get(id = project_id)
#         context['project']=project
#         projects = projects.exclude(id = project_id)
#         if request.POST.get('project') and request.POST.get('task') and request.POST.get('start_work') and request.POST.get('end_work') and request.POST.get('desc'):
#             task_obj = Tasks.objects.get(id=int(request.POST.get('task')))
#             start_work = datetime.fromisoformat(request.POST.get('start_work')).strftime('%Y-%m-%d %H:%M:%S')
#             end_work = datetime.fromisoformat(request.POST.get('end_work')).strftime('%Y-%m-%d %H:%M:%S')
#             desc = request.POST.get('desc')
#             if datetime.strptime(end_work, '%Y-%m-%d %H:%M:%S') > datetime.strptime(start_work, '%Y-%m-%d %H:%M:%S'):
#                 total_work_time = (datetime.strptime(end_work, '%Y-%m-%d %H:%M:%S') - datetime.strptime(start_work, '%Y-%m-%d %H:%M:%S'))
#                 decided_work_time = time(8, 30)  #datetime.strptime('08:30', '%H:%M').time()
#                 decided_work_time = datetime.combine(date.min, decided_work_time) - datetime.min
#                 total_decided_work_time = time(23,59)
#                 total_decided_work_time = datetime.combine(date.min, total_decided_work_time) - datetime.min
#                 if total_work_time > decided_work_time:
#                     work_time = '08:30'
#                     extra_time = str(total_work_time-decided_work_time)
#                     error = time(23, 59)  #datetime.strptime('08:30', '%H:%M').time()
#                     error = datetime.combine(date.min, error) - datetime.min
#                     if total_work_time > error:
#                         messages.error(request,f"Working Time is Too Much, Please Contact To HR!")
#                         return redirect('create_worklog')
#                 else:
#                     work_time = str(total_work_time)
#                     extra_time = '00:00'
#                 if Worklog.objects.filter(user=request.user,work_start__date=datetime.strptime(start_work, '%Y-%m-%d %H:%M:%S').date(),task=task_obj).exists():
#                     messages.warning(request,f"Worklog Already Exists for {task_obj.title}")
#                 else:
#                     w_objs = Worklog.objects.filter(user=request.user,work_start__date=datetime.strptime(start_work, '%Y-%m-%d %H:%M:%S').date())
#                     zero_time = time(0, 0)
#                     zero_time = datetime.combine(date.min, zero_time) - datetime.min
#                     for w_obj in w_objs:zero_time += datetime.combine(date.min, w_obj.active_time) - datetime.min
#                     if zero_time > total_decided_work_time:
#                         messages.error(request,f"Your Total Work Time for Today is Exceed, Please Contact To HR!")
#                         return redirect('create_worklog')
#                     else :
#                         worklog = Worklog(
#                             user = request.user,
#                             project=project,
#                             task=task_obj,
#                             work_start=start_work,
#                             work_end=end_work,
#                             work_time=work_time,
#                             extra_time=extra_time,
#                             active_time = str(total_work_time),
#                             describe=desc
#                             )
#                         if request.POST.get('task_status'):
#                             request.POST.get('task_status') == 'yes'
#                             task_obj.user_status = True
#                             task_obj.save()
#                         worklog.save()
#                         messages.success(request,f"New Work Log is Added for You!")
#                         return redirect('worklog')
#             else:
#                 messages.warning(request,f"Work End Time Must Be Greater Than Work Start Time")
        
#     context['projects'] = projects
#     print(request.POST)
#     return render (request,'common/worklog/create_worklog.html', context)

