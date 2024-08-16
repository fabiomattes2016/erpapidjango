from companies.views.base import Base
from companies.utils.exceptions import RequiredFields
from companies.utils.permissions import GroupsPermissions
from companies.serializers import GroupsSerializer
from accounts.models import Group, GroupPermissions
from rest_framework.views import Response
from rest_framework.exceptions import APIException
from django.contrib.auth.models import Permission


class Groups(Base):
    permission_classes = [GroupsPermissions]

    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)
        groups = Group.objects.filter(enterprise_id=enterprise_id).all()
        serializer = GroupsSerializer(groups, many=True)

        return Response({"groups": serializer.data})
    
    def post(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)
        name = request.data.get('name')
        permissions = request.data.get('permissions')

        if not name:
            raise RequiredFields
        
        created_group = Group.objects.create(
            name=name,
            enterprise_id=enterprise_id
        )

        if permissions:
            permissions = permissions.split(",") # 1,2 3,4 -> [1,2,3,4]

            for item in permissions:
                if type(item) != int:
                    created_group.delete()
                    raise APIException("Tipo de permissão inválida", code="invalid_type_permission")

                permission = Permission.objects.filter(id=item).exists()

                if not permission:
                    created_group.delete()
                    raise APIException("Permissão não existe", code="permission_not_exists")
                
                if not GroupPermissions.objects.filter(group_id=created_group.id, permission_id=item).exists():
                    GroupPermissions.objects.create(
                        group_id=created_group.id,
                        permission_id=item
                    )

        return Response({"success": True}, status=201)
    
    
class GroupDetail(Base):
    permission_classes = [GroupsPermissions]

    def get(self, request, group_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        self.get_group(group_id, enterprise_id)
        group = Group.objects.filter(id=group_id).first()
        serializer = GroupsSerializer(group)

        return Response({"group": serializer.data})
    
    def put(self, request, group_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        name = request.data.get('name')
        permissions = request.data.get('permissions')

        self.get_group(group_id, enterprise_id)

        if name:
            Group.objects.filter(id=group_id).update(name=name)

        GroupPermissions.objects.filter(group_id=group_id).delete()
                
        if permissions:
            permissions = permissions.split(",") # 1,2 3,4 -> [1,2,3,4]

            for item in permissions:
                if type(item) != int:
                    raise APIException("Tipo de permissão inválida", code="invalid_type_permission")

                permission = Permission.objects.filter(id=item).exists()

                if not permission:
                    raise APIException("Permissão não existe", code="permission_not_exists")
                
                if not GroupPermissions.objects.filter(group_id=group_id, permission_id=item).exists():
                    GroupPermissions.objects.create(
                        group_id=group_id,
                        permission_id=item
                    )
        
        
    
    def delete(self, request, group_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        Group.objects.filter(id=group_id, enterprise_id=enterprise_id).delete()

        return Response(status=204)
