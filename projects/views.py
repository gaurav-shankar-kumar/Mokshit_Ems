from django.contrib import messages
from django.shortcuts import render, redirect

from .models import Tasks, Project, Budget
from worklog .models import Worklog,Tasks
from users.models import User
from datetime import datetime
from django.contrib.auth.decorators import login_required
from admin_mokshit.permissions import administration_permission_required
# Create your views here.




@administration_permission_required()
def all_projects(request):
    projects = Project.objects.all()
    project_data = []
    for project in projects:
        task_complete = 0
        for task in project.task.all():
            if task.user_status:
                task_complete += 1
        print(project.task.all().count())
        try:
            task_complete_percent = (task_complete/project.task.all().count()) * 100
        except:
            task_complete_percent = 0
        project_data.append({'project':project,'task_complete':task_complete,'task_complete_percent':task_complete_percent})
    context = {'datas':project_data}
    return render(request,'admin/project.html',context)




@administration_permission_required()
def project_create(request):
    users = User.objects.exclude(role = "Trainee").exclude(role = "Junior Developer")
    context = {'users_obj':users}
    if request.POST:
        if len(request.POST.get('project_title')) > 0 and len(request.POST.get('project_start')) > 7 and len(request.POST.get('client_name')) > 0:
            project_title = request.POST.get('project_title')
            project_desc = None
            if len(request.POST.get('project_desc')):
                project_desc = request.POST.get('project_desc')
            project_start_date = datetime.strptime(request.POST.get('project_start'), '%d/%m/%Y')
            project_end_date = None
            if len(request.POST.get('project_end')) > 7:
                project_end_date = datetime.strptime(request.POST.get('project_end'), '%d/%m/%Y')
                if project_end_date <= project_start_date:
                    messages.error(request,f'Project Due Date Must Be Greater Than Project Start Time')
                    return render(request,'admin/new_project.html',context)
            client_name = request.POST.get('client_name')
            project = Project(title = project_title,description = project_desc,client = client_name,created_by = request.user, project_start = project_start_date, project_end = project_end_date)
            project.save()
            messages.success(request,f"New Project Added Successfully!")
            if request.POST.getlist('project_leader'):
                project_leader = request.POST.getlist('project_leader')
                user_list = users.filter(id__in=project_leader)
                project.project_controll_by.set(user_list)
            estimeted_budget = 0
            total_amount = 0
            if len(request.POST.get('estimeted_budget')) > 0:
                estimeted_budget = int(request.POST.get('estimeted_budget'))
            if len(request.POST.get('total_amount')) > 0:
                total_amount = int(request.POST.get('total_amount'))
            Budget.objects.create(project = project,estimeted_budget = estimeted_budget, total_amount = total_amount)
            return redirect ('project_details', pk=project.id)
    return render(request,'admin/new_project.html',context)


@login_required(login_url='/login/')
def project_details(request,pk=None):
    budget_obj = Budget.objects.get(project__id = pk)
    end_date = datetime.now().date()
    if budget_obj.project.project_end is not None:
        end_date = budget_obj.project.project_end.date()
    total_project_day = end_date - budget_obj.project.project_start.date()
    project_remaining_day = end_date - datetime.now().date()
    work_obj = Worklog.objects.filter(project__id = pk)
    context = {'budget_obj':budget_obj, 'work_obj':work_obj,'total_project_day':total_project_day.days,'project_remaining_day':project_remaining_day.days}
    return render(request,'admin/project_details.html',context)


@administration_permission_required()
def project_update(request,pk=None):
    users = User.objects.exclude(role = "Trainee").exclude(role = "Junior Developer")
    all_user = User.objects.all()
    budget_obj = Budget.objects.get(project__id = pk)
    if request.POST:
        project_title = request.POST.get('project_title')
        print(project_title)
        project_desc = None
        if len(request.POST.get('project_desc')):
            project_desc = request.POST.get('project_desc')
        project_start_date = datetime.strptime(request.POST.get('project_start'), '%d/%m/%Y')
        project_end_date = None
        if len(request.POST.get('project_end')) > 7:
            project_end_date = datetime.strptime(request.POST.get('project_end'), '%d/%m/%Y')
            if project_end_date <= project_start_date:
                messages.error(request,f'Project Due Date Must Be Greater Than Project Start Time')
                return render(request,'admin/project_edit.html',context)
        client_name = request.POST.get('client_name')
        project = Project.objects.get(id = pk)
        project.title = project_title
        project.description = project_desc
        project.client = client_name
        project.project_start = project_start_date
        project.project_end = project_end_date
        project.save()
        project_leader = request.POST.getlist('project_leader')
        project_member = request.POST.getlist('project_member')
        leader_list = users.filter(id__in=project_leader)
        member_list = all_user.filter(id__in=project_member)
        project.project_controll_by.set(leader_list)
        project.project_assign.set(member_list)
        estimeted_budget = 0
        total_amount = 0
        if len(request.POST.get('estimeted_budget')) > 0:
            estimeted_budget = int(request.POST.get('estimeted_budget'))
        if len(request.POST.get('total_amount')) > 0:
            total_amount = int(request.POST.get('total_amount'))
        budget_obj.project = project
        budget_obj.estimeted_budget = estimeted_budget
        budget_obj.total_amount = total_amount
        budget_obj.save()
        messages.success(request,f"Project Updated Successfully!")
        return redirect ('project_details', pk=pk)
    context = {'all_user':all_user,'users_obj':users,'budget_obj':budget_obj}
    return render(request,'admin/project_edit.html',context)


@login_required(login_url='/login/')
def task_board(request,pk=None):
    session_user = request.user
    today = datetime.now()
    context = {'today':today}

    all_projects_ = Project.objects.all()
    if session_user.is_admin or session_user.is_superuser:
        all_projects =  all_projects_
        context['add_task'] =True
        context['tasks'] = Tasks.objects.filter(on_delete = False).order_by('-created_at')
    elif all_projects_.filter(project_controll_by = session_user).exists():
        all_projects = all_projects_.filter(project_controll_by = session_user).all()
        context['add_task'] =True
        context['tasks'] = Tasks.objects.filter(on_delete = False,assign_by = session_user).order_by('-created_at')
    elif all_projects_.filter(project_assign = session_user).exists():
        all_projects = all_projects_.filter(project_assign = session_user).all()
        context['tasks'] = Tasks.objects.filter(on_delete = False,user = session_user).order_by('-created_at')
    
    if request.GET.get('project'):
        project_id = int(request.GET.get('project'))
        selected_project = all_projects.get(id=project_id)
        tasks = selected_project.task.filter(on_delete = False)
        context['tasks'] = tasks.order_by('-created_at')
        context['selected_project'] = selected_project
        
    elif pk is not None:
        selected_project = all_projects.get(id=pk)
        tasks = selected_project.task.filter(on_delete = False)
        context['tasks'] = tasks.order_by('-created_at')
        context['selected_project'] = selected_project
        
    if request.GET.get('project_leader'):
        selected_leader = int(request.GET.get('project_leader'))
        context['selected_leader'] = selected_leader
        tasks = selected_project.task.filter(on_delete = False).order_by('-created_at')
        context['tasks'] = tasks.filter(assign_by__id = selected_leader)
        
    if request.GET.get('project_member'):
        selected_member = int(request.GET.get('project_member'))
        context['selected_member'] = selected_member
        tasks = selected_project.task.filter(on_delete = False).order_by('-created_at')
        context['tasks'] = tasks.filter(user__id = selected_member)
        
    if request.POST.get('project_and_assign_user') and request.POST.get('task_title') and request.POST.get('task_desc') and request.POST.get('due_date'):
        project_and_assign_user = request.POST.get('project_and_assign_user').split(',')
        project_id = int(project_and_assign_user[0])
        assign_user_id = int(project_and_assign_user[1])
        title = request.POST.get('task_title')
        desc = request.POST.get('task_desc')
        due_date = datetime.strptime(request.POST.get('due_date'), '%Y-%m-%d')
        project_obj = all_projects.get(id=project_id)
        assign_to = project_obj.project_assign.get(id=assign_user_id)
        task = Tasks(title = title,description=desc,user=assign_to,assign_by=session_user,due_date=due_date)
        task.save()
        project_obj.task.add(task)
        messages.success(request,f'New Task Assign to {assign_to.get_full_name()}')
        return redirect('assign_task', pk = project_obj.id)

    
    if request.GET.get('task_delete'):
        task_id = int(request.GET.get('task_delete'))
        if Tasks.objects.filter(id = task_id).exists():
            task = Tasks.objects.get(id = task_id)
            task.on_delete = True
            task.save()
            return redirect('assign_task', pk = selected_project.id)
    # print(locals('session_user'),'<----')
    if 'all_projects' in locals():
        context['all_projects'] = all_projects
    return render (request,'admin/task_board.html',context)


