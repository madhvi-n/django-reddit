from core.serializers import ModelReadOnlySerializer
from groups.models import GroupMember, MemberRequest
from rest_framework import serializers


class MemberRequestReadOnlySerializer(ModelReadOnlySerializer):
    class Meta:
        model = MemberRequest
        fields = ("id", "group", "user", "is_approved")


class MemberRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberRequest
        fields = ("id", "group", "user", "is_approved")
        read_only_fields = ("id",)
        extra_kwargs = {"group": {"write_only": True}}

    def create(self, validated_data):
        request = self.context["request"]
        member_request = MemberRequest.objects.create(**validated_data)
        if member_request.group.group_type == "PUBLIC":
            member_request.is_approved = True
            member_request.save()
            if request.user:
                member, created = GroupMember.objects.get_or_create(
                    group=member_request.group, user=request.user
                )
        return member_request
