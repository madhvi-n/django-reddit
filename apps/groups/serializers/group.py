from core.serializers import ModelReadOnlySerializer
from groups.models import Group, GroupMember, MemberRequest
from rest_framework import serializers
from tags.serializers import TagReadOnlySerializer, TagSerializer


class GroupReadOnlySerializer(ModelReadOnlySerializer):
    topics = TagSerializer(required=False, many=True)
    group_type = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "description",
            "group_type",
            "topics",
            "archive_posts",
            "created_at",
        )

    def get_group_type(self, obj):
        if obj.group_type is not None:
            return obj.group_type.title()
        return None


class GroupReadOnlyLightSerializer(ModelReadOnlySerializer):
    class Meta:
        model = Group
        fields = (
            "id",
            "name",
        )


class GroupSerializer(serializers.ModelSerializer):
    topics = TagSerializer(required=False, many=True)
    members = serializers.SerializerMethodField()
    member_status = serializers.SerializerMethodField()
    group_type = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "description",
            "group_type",
            "topics",
            "archive_posts",
            "created_at",
            "members",
            "member_status",
        )

    def get_members(self, obj):
        if hasattr(obj, "members"):
            return obj.members.count()
        return 0

    def get_member_status(self, obj):
        request = self.context["request"]
        if request and request.user and request.user.is_authenticated:
            member_request = MemberRequest.objects.filter(
                group=obj, user=request.user
            ).first()
            if member_request is not None:
                from groups.serializers import MemberRequestReadOnlySerializer

                return MemberRequestReadOnlySerializer(member_request).data
        return None

    def get_group_type(self, obj):
        if obj.group_type is not None:
            return obj.group_type.title()
        return None


class GroupCreateSerializer(serializers.ModelSerializer):
    topics = TagSerializer(required=False, many=True)

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "description",
            "group_type",
            "topics",
            "archive_posts",
        )

    def create(self, validated_data):
        user = self.context["user"]
        group = Group.objects.create(**validated_data)
        member = GroupMember.objects.create(group=group, user=user, member_type="ADMIN")
        return group

    def update(self, instance, validated_data):
        instance.description = validated_data.get("description", instance.description)
        instance.group_type = validated_data.get("group_type", instance.group_type)
        instance.save()
        return instance


class GroupHeavySerializer(serializers.ModelSerializer):
    topics = TagSerializer(required=False, many=True)
    rules = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    member_status = serializers.SerializerMethodField()
    group_type = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "description",
            "group_type",
            "topics",
            "member_status",
            "archive_posts",
            "rules",
            "members_count",
            "created_at",
        )

    def get_rules(self, obj):
        if hasattr(obj, "rules"):
            from groups.serializers import GroupRuleSerializer

            return GroupRuleSerializer(obj.rules.all(), many=True).data
        return []

    def get_members_count(self, obj):
        if hasattr(obj, "members"):
            return obj.members.count()
        return 0

    def get_member_status(self, obj):
        request = self.context["request"]
        if request and request.user and request.user.is_authenticated:
            member_request = MemberRequest.objects.filter(
                group=obj, user=request.user
            ).first()
            if member_request is not None:
                from groups.serializers import MemberRequestReadOnlySerializer

                return MemberRequestReadOnlySerializer(member_request).data
        return None

    def get_group_type(self, obj):
        if obj.group_type is not None:
            return obj.group_type.title()
        return None
