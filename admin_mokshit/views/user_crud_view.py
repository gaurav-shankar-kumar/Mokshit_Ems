from django.urls import reverse
from django.shortcuts import render,get_object_or_404,redirect
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from users.models import User,Tech,User_Group
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from .. permissions import administration_permission_required



# @user_passes_test(is_admin)
# @login_required(login_url='/login/')
# @permission_required(['user.is_hr'],login_url="/login/")
# @admin_required()
@administration_permission_required()
def allusers(request):
    # bbds = request.user
    # bbds.is_superuser = True
    # bbds.save()
    context = {'Active_Users': True}
    alluser = User.objects.filter(is_active=True).exclude(is_superuser = True,is_admin=True)
    if request.GET.get('search'):
        search_query = request.GET.get('search')
        alluser = alluser.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) | Q(email__icontains=search_query) | Q(role__icontains=search_query))
        context['search_query'] = search_query
    if request.POST.get('inactive'):
        user_id = int(request.POST.get('inactive'))
        user_obj = alluser.get(id = user_id)
        user_obj.is_active = False
        user_obj.save()
        messages.success(request,f" 👍 {user_obj.email} Deactivated Successfully! ")
        return HttpResponseRedirect(reverse('all_users'))
        
    context['alluser'] = alluser
    return render (request,'admin/allusers.html', context)

@administration_permission_required()
def all_inactive_users(request):
    context = {'Active_Users': False}
    alluser = User.objects.filter(is_active=False)
    if request.GET.get('search'):
        search_query = request.GET.get('search')
        alluser = alluser.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) | Q(email__icontains=search_query) | Q(role__icontains=search_query))
        context['search_query'] = search_query
    if request.POST.get('active'):
        user_id = int(request.POST.get('active'))
        user_obj = alluser.get(id = user_id)
        user_obj.is_active = True
        user_obj.save()
        messages.success(request,f" 👍 {user_obj.email} Activated Successfully! ")
        return HttpResponseRedirect(reverse('all_inactive_users'))
    context['alluser'] = alluser
    return render (request,'admin/allusers.html', context)\


@administration_permission_required()
def update_user(request, pk=None):
    if pk is not None:
        user_obj = get_object_or_404(User, pk=pk)
        
        all_tech = Tech.objects.all()
        all_group = User_Group.objects.all()
        context = {
            'user_obj':user_obj,
            'all_tech':all_tech,
            'all_group':all_group
        }
        if request.POST:
            if request.FILES.get('profile'):
                user_obj.avatar = request.FILES.get('profile')
                messages.info(request,f"{user_obj.get_full_name()} Profile Photo Updated Successfully! ")
                

            if request.POST.get('first_name') : user_obj.first_name= request.POST.get('first_name')
            if request.POST.get('gender') : user_obj.gender = (request.POST.get('gender'))
            if request.POST.get('dob') : user_obj.dob =  datetime.strptime((request.POST.get('dob')), '%d/%m/%Y')
            if request.POST.get('emp_type') : user_obj.emp_type = context['emp_type'] = request.POST.get('emp_type')
            if request.POST.get('tech') : user_obj.tech.set(all_tech.filter(id__in = [eval(i) for i in (request.POST.getlist('tech'))]))
            if request.POST.get('address') : user_obj.address = (request.POST.get('address'))
            if request.POST.get('state') : user_obj.state = (request.POST.get('state'))
            if request.POST.get('zip') : user_obj.zip_code = (request.POST.get('zip'))

            if request.POST.get('last_name') : user_obj.last_name = request.POST.get('last_name')
            if request.POST.get('mobile') : user_obj.phone_number  = (request.POST.get('mobile'))
            if request.POST.get('group') : user_obj.group = all_group.get(id = int(request.POST.get('group')))
            if request.POST.get('doj') : user_obj.joining_date = datetime.strptime((request.POST.get('doj')), '%d/%m/%Y')
            if request.POST.get('role') : user_obj.role = request.POST.get('role')
            if request.POST.get('blood_group') : user_obj.blood_group = request.POST.get('blood_group')
            if request.POST.get('city') : user_obj.city = (request.POST.get('city'))
            if request.POST.get('country') : user_obj.country = request.POST.get('country')
            user_obj.save()
            if request.POST.get('go_to_salary'):
                messages.success(request,f"{user_obj.get_full_name()} Profile Updated Successfully! ")
                return redirect ('register_salary_details', pk=pk)
            if request.POST.get('go_to_bank'):
                messages.success(request,f"{user_obj.get_full_name()} Profile Updated Successfully! ")
                return redirect ('register_bank_details', pk=pk)
            if request.POST.get('submit_button'):
                messages.success(request,f"{user_obj.get_full_name()} Profile Updated Successfully! ")
                # return redirect ('update_user', pk= pk )
                return redirect ('all_users' )


    return render(request,'admin/updateuser.html',context)
