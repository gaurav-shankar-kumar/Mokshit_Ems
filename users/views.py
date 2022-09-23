
# Create your views here.
import email
from multiprocessing import context
from select import select
from django.conf import settings
from django.shortcuts import render,redirect
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import auth
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from .sendmail import Welcomemail
from projects.models import Project, Tasks
from leave_management.models import Leave
from admin_mokshit.views.salary_views import user_salary
from admin_mokshit.models import Salary, PaySlip
from datetime import datetime
from dateutil.relativedelta import relativedelta


from django.contrib.auth import logout 
from .models import User, User_Group,Tech,Bank_Details
from admin_mokshit.permissions import administration_permission_required

@login_required(login_url='/login/')
def ems(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_admin:
            return redirect('admin_dashboard')
        else:
            return redirect('emp_panel')


def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_admin:
            return redirect('admin_dashboard')
        else:
            return redirect('emp_panel')
        
    if request.method == 'POST':
        Email = request.POST['email']
        Password = request.POST['password']
        user = auth.authenticate(email=Email, password=Password)
        if user is not  None:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, f'Welcome Back {Email}')
                if request.GET.get('next'):
                    next = request.GET.get('next')
                    print(type(next),'<----next')
                    return redirect(next)
                elif user.is_superuser or user.is_admin:
                    return redirect('admin_dashboard')
                else:
                    return redirect('emp_panel')
            elif user.is_active == False:
                messages.error(request, f'Your Account is Not Active. Please Contact to Admin!')
                return redirect('login')
        elif User.objects.filter(email=Email).exists():
            messages.error(request, "Password Doesn't match")
            return redirect('login')
        else:
            messages.info(request, 'user not exist')
            return redirect('login')
    return render (request,'mokshitsite/login.html')


@administration_permission_required()
def register_user(request):
    all_users = User.objects.all()
    all_group = User_Group.objects.all()
    all_tech = Tech.objects.all()
    context = {'all_group':all_group,'all_tech':all_tech}
    if request.POST:
        if request.POST.get('first_name') : first_name = context['first_name'] = request.POST.get('first_name')
        if request.POST.get('last_name') : last_name = context['last_name'] = request.POST.get('last_name')
        if request.POST.get('gender') : gender = context['gender'] = (request.POST.get('gender'))
        if request.POST.get('dob') : dob = context['dob'] = (request.POST.get('dob'))
        if request.POST.get('emp_type') : emp_type = context['emp_type'] = (request.POST.get('emp_type'))
        if request.POST.get('tech') : tech = context['tech'] = [eval(i) for i in (request.POST.getlist('tech'))]
        if request.POST.get('address') : address = context['address'] = (request.POST.get('address'))
        if request.POST.get('state') : state = context['state'] = (request.POST.get('state'))
        if request.POST.get('zip') : zip = context['zip'] = (request.POST.get('zip'))


        if request.POST.get('mobile') : mobile = context['mobile'] = (request.POST.get('mobile'))
        if request.POST.get('group') : group = context['group'] = int(request.POST.get('group'))
        if request.POST.get('doj') : doj = context['doj'] = (request.POST.get('doj'))
        if request.POST.get('role') : role = context['role'] = request.POST.get('role')
        if request.POST.get('blood_group') : blood_group = context['blood_group'] = request.POST.get('blood_group')
        if request.POST.get('city') : city = context['city'] = (request.POST.get('city'))
        if request.POST.get('country') : country = context['country'] = request.POST.get('country')
        
        if request.POST.get('email') :
            email = context['email'] = request.POST.get('email')
            print(email)
            if all_users.filter(email = email).exists():
                context['email_validate'] = False
            else:
                context['email_validate'] = True
                if request.POST.get('password') and request.POST.get('submit_button'):
                    password = request.POST.get('password')
                    user = User.objects.create(email = email,first_name = first_name,password = make_password(password),dob = datetime.strptime(dob, '%d/%m/%Y'))
                    user
                    if first_name: user.first_name = first_name
                    if last_name : user.last_name = last_name
                    if gender : user.gender = gender #09/09/2022
                    if dob : user.dob = datetime.strptime(dob, '%d/%m/%Y')
                    if emp_type : user.emp_type = emp_type
                    if address : user.address = address
                    if state : user.state = state
                    if zip : user.zip_code = zip
                    if mobile : user.phone_number = mobile
                    if doj : user.joining_date = datetime.strptime(doj, '%d/%m/%Y')
                    if role : user.role = role
                    if blood_group : user.blood_group = blood_group
                    if city : user.city = city
                    if country : user.country = country
                    if group : user.group = all_group.get(id = group)
                    if tech :
                        tech_obj =  all_tech.filter(id__in = tech)
                        user.tech.set(tech_obj)
                    user.save()
                    Welcomemail(email,password,first_name)
                    messages.success(request,f"User Created Successfuly!")
                    return redirect ('register_bank_details', pk= user.id )
    return render (request,'admin/register_employee.html',context)

@administration_permission_required()
def register_bank_details(request,pk):
    print(request.POST)
    context = {}
    if pk is not None and User.objects.filter(id=pk):
        selected_user = User.objects.get(id = pk)
        context['selected_user'] = selected_user
        context['user_salary'] = selected_user.salary.last()
        context['bank_details'] = selected_user.bank_details.last()
        if request.POST:
            if request.POST.get('account_no'):
                account_no = request.POST.get('account_no')
                if request.POST.get('bank_name'):
                    bank_name = request.POST.get('bank_name')
                    if request.POST.get('ifsc'):
                        ifsc = request.POST.get('ifsc')
                        if request.POST.get('submit_bank'):
                            if Bank_Details.objects.filter(user = selected_user,bank_name = bank_name,ac_no = account_no,ifsc_no= ifsc).exists():
                                bank_obj = Bank_Details.objects.filter(user = selected_user,bank_name = bank_name,ac_no = account_no,ifsc_no= ifsc).last()
                            else:
                                bank_obj = Bank_Details.objects.create(user = selected_user,bank_name = bank_name,ac_no = account_no,ifsc_no= ifsc,action_by = request.user)
                                bank_obj
                            if request.POST.get('pf'):
                                pf = request.POST.get('pf')
                                bank_obj.pf_no = pf
                            bank_obj.save()
                            messages.success(request,f"{selected_user.get_full_name()} Bank Details Saved Successfuly!")
                            return redirect('register_salary_details', pk=selected_user.id)
    return render (request,'admin/register_bank_details.html',context)

@administration_permission_required()
def register_salary_details(request,pk):
    today = datetime.now()
    print(request.POST)
    context = {'today':today}
    if pk is not None and User.objects.filter(id=pk):
        selected_user = User.objects.get(id = pk)
        context['selected_user'] = selected_user
        last_date = today
        if selected_user.salary.exists():
            context['user_salary'] = user_salary = selected_user.salary.all()
            last = user_salary.last()
            total_basic = last.basic
            last_date = last.apply_from + relativedelta(months=1)
            if last.increament != 0:
                total_basic = (last.basic * last.increament/100) + last.basic
            context['total_basic'] = total_basic
        context['last_date'] = last_date
        if request.POST.get('month') :
            select_month = request.POST.get('month').split('-')
            date = datetime(int(select_month[0]), int(select_month[1]), 1).date()
            if selected_user.salary.exists() and user_salary.filter(apply_from__year__gte = select_month[0],apply_from__month__gte = select_month[1]).exists():
                messages.warning(request,f"Salary Applied Moth Must Be Greater Than All Previous!")
            if request.POST.get('basic') and request.POST.get('submit_salary'):
                salary_obj = Salary.objects.create(user = selected_user,basic = float(request.POST.get('basic')),apply_from = date,action_by = request.user)
                salary_obj
                if request.POST.get('hra') :
                    salary_obj.hra = float(request.POST.get('hra'))
                if request.POST.get('increament') :
                    salary_obj.increament = float(request.POST.get('increament'))
                salary_obj.save()
                messages.success(request,f"New Salary has been Added and will be Apply From {select_month[1]}-{select_month[0]} ")
                return redirect ('user_profile', pk=selected_user.id)
    return render (request,'admin/register_salary_details.html',context)

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    messages.success(request, "Log Out Sucessfully")
    return redirect("login")

@administration_permission_required()
def register__new_user(request):
    if request.method == 'POST':
        FirstName = request.POST['fname']
        LastName = request.POST['lname']
        Mobile = request.POST['mobile']
        Gender = request.POST['gender']
        Email = request.POST['email']
        Password = request.POST['password']
        Designation = request.POST['designation']
        Role = request.POST['role']
        Salary = int(request.POST['salary'])
        Doj = request.POST['doj']
        Emptype = request.POST['emptype']
        Position = request.POST['position']
        Technology = request.POST['technology']

        User.objects.create(first_name=FirstName,last_name=LastName,phone_number=Mobile,gender=Gender,email=Email,password=make_password(Password),designation=Designation,role=Role,joining_date=Doj,emp_type=Emptype,position=Position,is_staff = True)
        messages.success(request,f'New User Added Sucessfully!')
        # sending the credential through mail
        
        Welcomemail(Email,Password,FirstName)
        messages.success(request,f'Welcome Email has been Sent to {Email}') 
        return redirect ('admin_dashboard')
    else:
        pass
    return render (request,'admin/register.html')

@administration_permission_required()
def reset_password(request,pk):
    user = User.objects.get(id = pk)
    if request.method == 'POST':
        password = request.POST.get('password')
        user.password = make_password(password)
        user.save()
        subject = 'Your Password has changed Sucessfully'
        message = f'Hi  Your email is {user.email} and new password is {password} '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail( subject, message, email_from, recipient_list )
        messages.info(request, 'User Password has been changed and Mail sucessfully')
        return redirect('update_user', pk=pk)
    return render(request,'admin/passwordchange.html')

@login_required(login_url='/login/')
def profile(request,pk=None):
    context = {}
    if request.GET.get('tab'):
        context['tab'] = request.GET.get('tab')
    # messages.error(request,f"Welcome to The Profile secetion")
    selected_user = User.objects.get(id = request.user.id)
    if pk is not None and User.objects.filter(id = pk).exists() and selected_user.is_admin and selected_user.is_superuser:
        selected_user = User.objects.get(id = pk)

    projects = Project.objects.filter(project_assign__id=selected_user.id)
    tasks = Tasks.objects.filter(user = selected_user)
    leaves = Leave.objects.filter(user = selected_user).order_by('-startdate')
    context['selected_user'] = selected_user
    context['tasks'] = tasks
    context['projects'] = projects
    context['leaves'] = leaves
    context['salary'] = user_salary(selected_user)
    print(context['salary'])
    return render (request,'common/profile/profile.html',context)