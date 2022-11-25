from rest_framework import permissions
from groups.models import Group


class HasGroupEditPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        try:
            group_id = request.parser_context['kwargs']['pk']
            group = Group.objects.filter(id=group_id)
        except Exception as e:
            return False
        return user.has_perm('edit_groups', group)


class HasGroupDeletePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        try:
            group_id = request.parser_context['kwargs']['pk']
            group = Group.objects.filter(id=group_id)
        except Exception as e:
            return False
        return user.has_perm('delete_groups', group)


class HasAddMembersPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        try:
            member_id = request.parser_context['kwargs']['pk']
            member = Group.objects.filter(id=member_id)
        except Exception as e:
            return False
        return user.has_perm('add_members', member)
