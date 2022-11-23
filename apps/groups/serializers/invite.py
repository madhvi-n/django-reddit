from rest_framework import serializers
from core.serializers import ModelReadOnlySerializer
from groups.models import GroupInvite


class GroupInviteReadOnlySerializer(ModelReadOnlySerializer):
    class Meta:
        model = GroupInvite
        fields = ('id', 'group', 'created_by', 'user', 'invite_as')


class GroupInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInvite
        fields = ('id', 'group', 'created_by', 'user', 'invite_as')
        read_only_fields = ('id',)
        extra_kwargs = {
            'group': {'write_only': True},
            'user': {'write_only': True}
        }
