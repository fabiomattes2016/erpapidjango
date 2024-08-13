from rest_framework import permissions
from accounts.models import UserGroups, GroupPermissions
from django.contrib.auth.models import Permission


def check_permissions(user, method, permission_to):
    if not user.is_authenticated:
        return False
    
    if user.is_owner:
        return True
    
    required_permission = f'view_{permission_to}'
    
    match method:
        case 'GET':
            required_permission = f'view_{permission_to}'
        case 'POST':
            required_permission = f'add_{permission_to}'
        case 'PUT':
            required_permission = f'change_{permission_to}'
        case 'PATCH':
            required_permission = f'change_{permission_to}'
        case 'DELETE':
            required_permission = f'delete_{permission_to}'
        case _:
            required_permission = f'view_{permission_to}'
    
    groups = UserGroups.objects.values('group_id').filter(user_id=user.id).all()
    
    for group in groups:
        permissions_group = GroupPermissions.objects.values('permission_id').filter(group_id=group['group_id']).all()
        
        for permission in permissions_group:
            if Permission.objects.filter(id=permission['permission_id'], codename=required_permission).exists():
                return True

class EmployeesPermisison(permissions.BasePermission):
    message = "O funcionário não tem permissão para gerenciar outros funcionários"
    
    def has_permission(self, request, view):
        return check_permissions(request.user, request.method, permission_to='employee')
