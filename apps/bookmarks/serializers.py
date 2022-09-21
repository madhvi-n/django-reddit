from rest_framework import serializers

from bookmarks.models import PostBookmark


class PostBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostBookmark
        fields = ('id', 'post', 'user')
        read_only_fields = ('id',)
        extra_kwargs = {
            'post': {'write_only': True}
        }

    def create(self, validated_data):
        bookmark = PostBookmark.objects.create(**validated_data)
        return bookmark


class PostBookmarkLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostBookmark
        fields = ('id', 'user')
        read_only_fields = ('id',)
