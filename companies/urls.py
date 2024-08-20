from django.urls import path

from companies.views.employees import *
from companies.views.permissions import *
from companies.views.groups import *
from companies.views.tasks import *

urlpatterns = [
    # Employess endpoints
    path('employees', Employees.as_view()),
    path('employees/<int:employee_id>', EmployeeDetail.as_view()),

    # Groups & Permissions endpoints
    path('groups', Groups.as_view()),
    path('groups/<int:group_id>', GroupDetail.as_view()),
    path('permissions', PermissionDetail.as_view()),

    # Tasks
    path('tasks', Tasks.as_view()),
    path('tasks/<int:task_id>', TaskDetail.as_view()),
]