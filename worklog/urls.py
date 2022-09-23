from django.urls import path
from . import views


urlpatterns = [
   
    path('',views.worklog, name ='worklog'),
    # path('add-worklog',views.create_worklog, name ='create_worklog'),
   
    
]
