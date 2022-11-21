from rest_framework import serializers
from core.serializers import ModelReadOnlySerializer
from groups.models import MemberRequest


class MemberRequestReadOnlySerializer(ModelReadOnlySerializer):
    class Meta:
        model = MemberRequest
        fields = ('id', 'group', 'user', 'is_approved')


class MemberRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberRequest
        fields = ('id', 'group', 'user', 'is_approved')
