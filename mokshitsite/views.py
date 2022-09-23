from django.shortcuts import render,redirect
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import  auth

from .models import Contactlist
from django.core.mail import send_mail
from users.models import User
from admin_mokshit.models import Contacts,Site_Team,Client,Count,Portfolio
from projects.models import Project




def home(request):
    contact = Contacts.objects.filter().last()
    teams = Site_Team.objects.filter(is_active = True,user__is_active=True).order_by('sort')
    clients = Client.objects.all().order_by('-id')
    count_obj = Count.objects.filter().last()
    # projects = Project.objects.filter(on_delete=False)
    portfolios = Portfolio.objects.all()
    print(portfolios.values_list('project'))
    projects = set()
    for obj in portfolios:projects.add(obj.project)
    


    context = {
        'teams':teams,
        'contact':contact,
        'clients':clients,
        'count':count_obj,
        'projects':list(projects),
        'portfolios':portfolios
    }
    if request.POST:
        print(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contactlist.objects.create(name=name,Email=email,subject=subject,Message=message)
        messages.success(request,f'{name} Message has been Delevered!')

        send_mail(
            subject, #subject of mail 
            name+message, 
            email,
            ['gaurav.mit.dev@gmail.com']
        )
        # contact = Contactlist(First_name=First_Name,Last_name=Last_Name,mobile=Mobile,Email=Email,Message=Message)
        # contact.save()

    return render(request,'mokshitsite/mokshit.html',context)


def about(request):
    return render(request,'mokshitsite/about_us.html')

def services(request):
    return render(request,'mokshitsite/services.html')

# Create your views here.
def contact(request):
    if request.method == "POST":
        First_Name = request.POST['fstname']
        Last_Name = request.POST['lstname']
        Mobile = request.POST['mobileno']
        Email = request.POST['email']
        Message = request.POST['message'] 
        
        # send mail 
        send_mail(
            'Message from' +  First_Name, #subject of mail 
            Message, 
            Email,
            ['mahipuja786@gmail.com']
        )
        contact = Contactlist(First_name=First_Name,Last_name=Last_Name,mobile=Mobile,Email=Email,Message=Message)
        contact.save()
        
        context = {
            'fstname':First_Name,
        }     
    return render(request,'mokshitsite/contactus.html')
        
    
   


def carrer(request):
    return render (request,'mokshitsite/carrer.html')



  
   

