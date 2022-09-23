from dataclasses import field
from .models import Contacts,Site_Team,Count,Portfolio
from django.forms import ModelForm


class ContactsForm(ModelForm):
    class Meta:
        model = Contacts
        fields = ['phone_no','email','address','landmark','city','state','zip','embed_link','twitter_link','fb_link','insta_link','skype_link','linkedin_link']


class Site_Team_Form(ModelForm):
    class Meta:
        model = Site_Team
        fields = ['user','title','sort']

class CountForm(ModelForm):
    class Meta:
        model = Count
        fields = ['happy_client','total_project','hours_support','hard_worker']


class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = ['project','title','img_title','image']