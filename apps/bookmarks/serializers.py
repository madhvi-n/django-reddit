from bookmarks.models import PostBookmark
from core.serializers import ModelReadOnlySerializer
from rest_framework import serializers


class PostBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostBookmark
        fields = ("id", "post", "user")
        read_only_fields = ("id",)
        extra_kwargs = {"post": {"write_only": True}}

    def create(self, validated_data):
        bookmark = PostBookmark.objects.create(**validated_data)
        return bookmark


class PostBookmarkLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostBookmark
        fields = ("id", "user")
        read_only_fields = ("id",)


class PostBookmarkReadOnlySerializer(ModelReadOnlySerializer):
    post = serializers.SerializerMethodField()

    class Meta:
        model = PostBookmark
        fields = ("id", "post", "user")

    def get_post(self, obj):
        if hasattr(obj, "post"):
            from posts.serializers import PostReadOnlySerializer

            return PostReadOnlySerializer(obj.post).data
        return None
