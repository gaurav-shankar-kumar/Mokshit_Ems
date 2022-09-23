from django.urls import path
from .views import main_views,salary_views,user_crud_view,pay_slip_views,site


urlpatterns = [
    path('admindashboard/',main_views.admindashboard, name = 'admin_dashboard'),
    path('allusers/',user_crud_view.allusers, name ='all_users'),
    path('in-active-users/',user_crud_view.all_inactive_users, name ='all_inactive_users'),
    # path('delete_user/<int:id>/',main_views.Delete_user, name ='delete_user'),
    path('<int:pk>/',user_crud_view.update_user, name ='update_user'),
    path('salary/', salary_views.salary_management, name = 'salary_management'),
    path('payslip/<int:pk>/', pay_slip_views.pay_slip, name = 'pay_slip'),
    path('payslip/<int:pk>/<int:pay_slip_id>/', pay_slip_views.pay_slip_details, name = 'pay_slip_details'),
    path('settings/', site.Site_settings.contact_service, name = 'site_settings'),
    path('settings/team', site.Site_settings.team, name = 'site_settings_team'),
    path('settings/team/<int:pk>/edit', site.Site_settings.team, name = 'site_settings_team_edit'),
    path('settings/clients', site.Site_settings.clients, name = 'site_settings_clients'),
    path('settings/clients/<int:pk>/', site.Site_settings.clients, name = 'site_settings_clients'),
    path('settings/portfolio', site.Site_settings.portfolio, name = 'site_settings_portfolio'),
    path('settings/portfolio/<int:pk>/edit', site.Site_settings.portfolio, name = 'site_settings_portfolio_edit'),
    path('settings/count', site.Site_settings.count, name = 'site_settings_count'),
]