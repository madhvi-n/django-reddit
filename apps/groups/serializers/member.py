from rest_framework import serializers
from core.serializers import ModelReadOnlySerializer
from groups.models import GroupMember
from groups.serializers import GroupReadOnlyLightSerializer


class GroupMemberReadOnlySerializer(ModelReadOnlySerializer):
    group = GroupReadOnlyLightSerializer()

    class Meta:
        model = GroupMember
        fields = ('id', 'group', 'user', 'member_type', 'status')


class GroupMemberSerializer(serializers.ModelSerializer):
    group = GroupReadOnlyLightSerializer()

    class Meta:
        model = GroupMember
        fields = ('id', 'group', 'user', 'member_type', 'status')
