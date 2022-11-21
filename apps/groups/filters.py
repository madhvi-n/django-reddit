import django_filters
from groups.models import Group, GroupMember


class GroupFilterSet(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Group
        fields = ('name', 'description', 'group_type', 'members__user', 'members__member_type')


class GroupMemberFilterSet(django_filters.rest_framework.FilterSet):
    class Meta:
        model = GroupMember
        fields = ('member_type', 'group', 'status', 'user')
