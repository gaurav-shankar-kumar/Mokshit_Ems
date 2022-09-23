from django.urls import path
from . import views

urlpatterns = [
        path('',views.all_projects, name = 'all_projects'),
        # path('details/',views.all_projects, name = 'all_projects'),
        path('details/<int:pk>',views.project_details, name = 'project_details'),
        path('update/<int:pk>',views.project_update, name = 'project_update'),
        path('new-project/',views.project_create, name = 'project_create'),
        path('task-board/',views.task_board, name = 'task_board'),
        path('task-board/<int:pk>',views.task_board, name = 'assign_task'),
        # path('all-holiday/',views.all_holidays, name = 'all_holiday'),

]
 