from django.urls import path
from employee import views
from admin_mokshit.views import pay_slip_views

urlpatterns = [
        path('emppanel/',views.emppanel, name = 'emp_panel'),
        # path('alltask/',views.emptasks, name = 'alltask'),
        path('payslip/',pay_slip_views.pay_slip, name = 'payslip'),

]
 