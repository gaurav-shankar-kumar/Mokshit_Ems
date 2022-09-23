from django.urls import path
from holidays import views

urlpatterns = [
        path('addholiday/',views.add_holiday, name = 'add_holiday'),
        path('all-holiday/',views.all_holidays, name = 'all_holiday'),

]
 