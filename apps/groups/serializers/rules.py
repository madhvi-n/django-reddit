from rest_framework import serializers
from core.serializers import ModelReadOnlySerializer
from groups.models import GroupRule


class GroupRuleReadOnlySerializer(ModelReadOnlySerializer):
    class Meta:
        model = GroupRule
        fields = ('id', 'group', 'title', 'rule_type', 'description')


class GroupRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupRule
        fields = ('id', 'group', 'title', 'rule_type', 'description')
