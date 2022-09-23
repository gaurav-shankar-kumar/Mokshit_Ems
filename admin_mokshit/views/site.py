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

from projects.models import Project
from ..models import Contacts,Client,Site_Team,Count,Portfolio
from ..forms import ContactsForm,Site_Team_Form,CountForm,PortfolioForm

class Site_settings:
    def contact_service(request):
        contact = Contacts.objects.filter().last()
        context = {'contact_tab':True,'contact':contact}
        if request.POST:
            form = ContactsForm(request.POST)
            if contact is not None:
                form = ContactsForm(request.POST,instance=contact)
            if form.is_valid:
                print('form is valid')
                form.save()
                messages.success(request,'Data Updated Sucessfully')
        return render(request,'site_settings/site_settings.html',context)
    def team(request,pk=None):
        teams = Site_Team.objects.all().order_by('sort')
        print(teams.values_list('user',flat=True))
        selects = User.objects.filter(is_active=True).exclude(id__in= teams.values_list('user',flat=True))
        context = {'team_tab':True,'team':teams,'selects':selects}
        form = Site_Team_Form(request.POST)
        if pk is not None:
            a_team = teams.get(id=pk)
            form = Site_Team_Form(request.POST,instance=a_team)
            context['a_team'] = a_team
        if request.POST:
            if form.is_valid:
                form.save()
                messages.success(request,'Team Data Saved Successfully!')
                return redirect('site_settings_team')
        if request.GET.get('delete'):
            d_id = int(request.GET.get('delete'))
            d_obj =  teams.filter(id=d_id).first()
            if d_obj is not None:
                d_obj.delete()
                messages.warning(request,'Team Data Has Been Deleted!')
            return redirect('site_settings_team')
        return render(request,'site_settings/site_settings.html',context)
    def clients(request,pk=None):
        client = Client.objects.all().order_by('name')
        context = {'client_tab':True,'clients':client}
        if pk is not None:
            client_obj = client.get(id = pk)
            context['client'] = client_obj
        if request.GET.get('delete'):
            d_id = int(request.GET.get('delete'))
            print(d_id)
            d_obj = client.filter(id=d_id).first()
            if d_obj is not None:
                print(d_id)
                d_obj.delete()
                messages.warning(request,'Client Data Has Been Deleted!')
            return redirect('site_settings_clients')
        if request.POST:
            name = request.POST.get('name')
            title = request.POST.get('title')
            quote = request.POST.get('quotes')
            if request.POST.get('id'):
                id  = int(request.POST.get('id'))
                print('id--->',id)
                client_data = client.get(id = id)
                client_data.name = name
                client_data.title = title
                client_data.quotes = quote
                messages.success(request,'Client Updated Successfully!')
            else:
                client_data = Client.objects.create(name = name,title=title,quotes = quote)
                messages.success(request,'New Client Added Successfully!')
            if request.FILES:
                image = request.FILES.get('image')
                client_data.image = image
            client_data.save()
            return redirect('site_settings_clients')
        return render(request,'site_settings/site_settings.html',context)
    def portfolio(request,pk=None):
        projects = Project.objects.all()
        portfolios =  Portfolio.objects.all()
        all_portfolio = portfolios
        context = {'projects':projects,'portfolios_tab':True}
        if request.GET.get('delete'):
            d_id = int(request.GET.get('delete'))
            d_obj = portfolios.filter(id=d_id).first()
            if d_obj is not None:
                d_obj.delete()
                messages.warning(request,'Portfolio Data Has Been Deleted!')
                return redirect ('site_settings_portfolio')
        
        if request.GET.get('select_project'):
            context['selected_project'] = project_id = int(request.GET.get('select_project'))
            print('------->',project_id)
            all_portfolio = portfolios.filter(project__id = project_id)
        context['portfolios'] = all_portfolio
        
        if pk is not None:
            portfolio = portfolios.get(id=pk)
            context['portfolio'] = portfolio
            # context['selected_project'] = projects.get(id = pro)
        if request.POST:
            form = PortfolioForm(request.POST,request.FILES)
            if request.POST.get('id'):
                port_id = int(request.POST.get('id'))
                port_obj = portfolios.get(id= port_id)
                form = PortfolioForm(request.POST,request.FILES,instance=port_obj)
            if form.is_valid:
                form.save()
                messages.success(request,'Portfolio Data Saved Successfully!')
            return redirect('site_settings_portfolio')
        if request.GET.get('delete'):
            d_id = int(request.GET.get('delete'))
            d_obj = portfolios.filter(id=d_id).first()
            if d_obj is not None:
                d_obj.delete()
                messages.warning(request,'Portfolio Data Has Been Deleted!')

        return render(request,'site_settings/site_settings.html',context)
    
    def count(request):
        count_obj = Count.objects.filter().last()
        form = CountForm(request.POST)
        if request.POST:
            if request.POST.get('id'):
                form = CountForm(request.POST,instance=count_obj)
            if form.is_valid:
                form.save()
                messages.success(request,'Data Saved Successfully!')
                return redirect('site_settings_count')
        if count_obj is not None:
            context = {'count':count_obj}
        else:
            context= {'count':True}
        return render(request,'site_settings/site_settings.html',context)