from django.urls import path
from users import views


urlpatterns = [
   
    path('ems/',views.ems, name ='ems'),
    path('login/',views.login, name ='login'),
    path('logout/',views.logout_view, name ='logout'),
    path('register_user/',views.register__new_user, name = 'register'),
    path('register/',views.register_user, name = 'new_employee'),
    path('user-bank-details/<int:pk>/',views.register_bank_details, name = 'register_bank_details'),
    path('user-salary-details/<int:pk>/',views.register_salary_details, name = 'register_salary_details'),
    # path('user-finance-details/<int:pk>/',views.register_bank_salary, name = 'register_bank_salary'),
    path('Changepassword/<int:pk>',views.reset_password, name = 'change_password'),
    path('profile/', views.profile, name = 'profile'),
    path('profile/<int:pk>/', views.profile, name = 'user_profile')
    
]
