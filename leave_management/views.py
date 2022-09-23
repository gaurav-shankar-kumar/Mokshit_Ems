from audioop import reverse
from datetime import datetime
from multiprocessing import context
import re
from django.shortcuts import render,redirect
from users.models import User
from .models import Leave ,leavetype_choise
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from admin_mokshit.permissions import administration_permission_required
# Create your views here.

@login_required(login_url='/login/')
def leaveapplicaion(request):
    
    # ltypes = Leave.objects.filter(leave_type='Sick')
    context = {
    }
    if request.method == "POST":
        Leave_type = request.POST['leave_type']
        Description = request.POST['description'] 
        Start_date = request.POST['start_date']
        End_date = request.POST['end_date']
        types = Leave(user=request.user, leave_type=Leave_type,description=Description,startdate=Start_date,enddate=End_date )
        types.save()
        messages.success(request, f'Your Leave Appplication Has Been Submited!')
    return redirect('leave_view')
    # return render(request,'employee/leaveform.html',context)

@administration_permission_required()
def allleaves(request):
    today = datetime.now().date()
    context = {'today':today}
    all_leaves = Leave.objects.filter(on_delete=False)
    if request.GET.get('search'):
        print(request.GET.get('search'))
        search_query = request.GET.get('search')
        context['search_query'] = search_query
        all_leaves = Leave.objects.filter(Q(user__first_name__icontains=search_query) | Q(user__last_name__icontains=search_query) | Q(user__email__icontains=search_query) | Q(leave_type__icontains=search_query) | Q(description__icontains=search_query) | Q(approved_by__first_name__icontains=search_query) | Q(approved_by__last_name__icontains=search_query) | Q(approved_by__email__icontains=search_query) )


    
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('id') and request.POST.get('action1'):
            id = int(request.POST.get('id'))
            action1 = str(request.POST.get('action1'))
            leave = all_leaves.get(id = id )
            if request.POST.get('remark'):
                leave.remarks = request.POST.get('remark')
            leave.leave_status = action1
            leave.approved_by = request.user
            leave.save()
        elif request.POST.get('id') and request.POST.get('action'):
            id = int(request.POST.get('id'))
            action = str(request.POST.get('action'))
            leave = all_leaves.get(id = id )
            if request.POST.get('remark'):
                leave.remarks = request.POST.get('remark')
            leave.leave_status = action
            leave.approved_by = request.user
            leave.save()
    context['all_leaves'] = all_leaves
    return render(request,'admin/all_leaves.html',context)

@login_required(login_url='/login/')   
def leaveview(request):
    today = datetime.now().date()
    leave_app = Leave.objects.filter(user=request.user)
    context ={
        'leaves':leave_app,
        'today': today
    }
    return render(request,'employee/myleaves.html',context)

@administration_permission_required()
def calender_leave_view(requset):
    today = datetime.now().date()
    context = {'today':today}
    all_leaves = Leave.objects.filter(on_delete = False)
    context['all_leaves'] = all_leaves
    return render  (requset,'admin/calender_leave.html',context)