
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from admin_mokshit.views.main_views import page_not_found_view,server_error


urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('', include('mokshitsite.urls')),
    path('admin/', include('admin_mokshit.urls')),
    path('',include('users.urls')),
    path('',include('employee.urls')),
    path('leave/',include('leave_management.urls')),
    path('holiday/',include('holidays.urls')),
    path('projects/',include('projects.urls')),
    path('worklog/',include('worklog.urls')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



handler404 = page_not_found_view
handler500 = server_error
