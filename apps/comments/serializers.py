from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comments.models import PostComment, PostCommentVote
from profiles.serializers import UserSerializer


class PostCommentLightSerializer(serializers.ModelSerializer):
    comment = serializers.ReadOnlyField(source='_get_comment')

    class Meta:
        model = PostComment
        fields = ('id', 'comment', 'created_at')


class PostCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    comment = serializers.ReadOnlyField(source='_get_comment')
    votes = serializers.ReadOnlyField(source='_get_score')
    mentioned_users = UserSerializer(many=True, required=False)
    edited = serializers.ReadOnlyField(source='is_edited')
    child_count = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = (
            'id', 'user', 'mentioned_users', 'comment', 'votes',
            'flair', 'created_at', 'edited', 'is_removed',
            'updated_at', 'is_nesting_permitted', 'child_count', 'parent'
        )
        read_only_fields = (
            'id', 'created_at', 'updated_at', 'child_count')

    def get_child_count(self, obj):
        return PostComment.objects\
            .filter(parent=obj)\
            .exclude(is_removed=True)\
            .count()


class PostCommentCreateSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(max_length=3000, min_length=4)
    mentioned_users = UserSerializer(many=True, required=False)
    edited = serializers.ReadOnlyField(source='is_edited')
    child_count = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = (
            'id', 'user', 'comment', 'mentioned_users', 'post',
            'parent', 'is_nesting_permitted', 'child_count', 'edited'
        )
        read_only_fields = ('mentioned_users', 'child_count')
        extra_kwargs = {
            'post': {'write_only': True}
        }

    def create(self, validated_data):
        comment = validated_data.pop('comment')
        validated_data['_comment'] = comment
        comment = PostComment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        comment = validated_data.pop('comment')
        validated_data['_comment'] = comment
        instance._comment = comment
        instance.save()
        return instance

    def get_child_count(self, obj):
        return 0


class PostCommentVoteSerializer(serializers.ModelSerializer):
    post_comment = PostCommentLightSerializer()

    class Meta:
        model = PostCommentVote
        fields = ('id', 'vote', 'created_at', 'post_comment')
