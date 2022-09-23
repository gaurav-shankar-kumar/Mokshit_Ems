from django.urls import path
from leave_management import views

urlpatterns = [
        path('leaveapp/',views.leaveapplicaion, name = 'leave_application'),
        path('allleaveapp/',views.allleaves, name = 'all_leaves'),
        path('leaveview/',views.leaveview, name ='leave_view'),
        path('calendar/',views.calender_leave_view, name ='calender_leave'),

]
 