from core.serializers import ModelReadOnlySerializer
from rest_framework import serializers

from .models import Tag, TagType


class TagTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagType
        fields = (
            "id",
            "title",
        )
        read_only_fields = ("id",)


class TagSerializer(serializers.ModelSerializer):
    tag_type = TagTypeSerializer()

    class Meta:
        model = Tag
        fields = ("id", "name", "tag_type")
        read_only_fields = ("id",)


class TagReadOnlySerializer(ModelReadOnlySerializer):
    class Meta:
        model = Tag
        fields = "__all__"
