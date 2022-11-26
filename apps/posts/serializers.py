from rest_framework import serializers
from posts.models import Post, PostVote
from profiles.serializers import UserSerializer, UserReadOnlySerializer
from tags.serializers import TagSerializer
from comments.models import PostComment
from bookmarks.models import PostBookmark
from bookmarks.serializers import PostBookmarkLightSerializer
from django.db.models import Sum
from core.serializers import ModelReadOnlySerializer
from groups.serializers import GroupSerializer, GroupReadOnlyLightSerializer


class PostVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVote
        fields = ('id', 'vote')


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    votes = serializers.ReadOnlyField(source='_get_score')
    user_vote = serializers.SerializerMethodField()
    user_bookmark = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    tags = TagSerializer(required=False, many=True)
    group = GroupReadOnlyLightSerializer(required=False)

    class Meta:
        model = Post
        fields = (
            'title', 'content', 'uuid', 'author', 'votes',
            'comments', 'created_at', 'updated_at', 'tags',
            'user_vote', 'user_bookmark', 'group', 'status',
        )

    def get_comments(self, obj):
        return PostComment.objects.filter(post=obj, is_removed=False).count()

    def get_user_vote(self, obj):
        request = self.context.get('request', None)
        if request is not None and request.user.is_authenticated:
            votes = PostVote.objects.filter(post=obj, user=request.user)\
                .order_by('-updated_at')
            if votes.exists():
                return PostVoteSerializer(votes.first()).data
        return None

    def get_user_bookmark(self, obj):
        request = self.context.get('request', None)
        if request is not None and request.user.is_authenticated:
            bookmarks = PostBookmark.objects.filter(post=obj, user=request.user)\
            .order_by('-updated_at')
            if bookmarks.exists():
                return PostBookmarkLightSerializer(bookmarks.first()).data
        return None


class PostReadOnlySerializer(ModelReadOnlySerializer):
    author = UserReadOnlySerializer()
    group = GroupReadOnlyLightSerializer(required=False)
    votes = serializers.ReadOnlyField(source='_get_score')

    class Meta:
        model = Post
        fields  = (
            'uuid', 'title', 'content', 'author', 'votes',
            'created_at', 'group', 'status'
        )


class PostVoteHeavySerializer(serializers.ModelSerializer):
    post = PostReadOnlySerializer()

    class Meta:
        model = PostVote
        fields = ('id', 'vote', 'post', 'created_at')


class PostEditSerializer(serializers.ModelSerializer):
    tags = TagSerializer(required=False, many=True)

    class Meta:
        model = Post
        fields = (
            'uuid', 'title', 'content', 'author', 'tags',
            'created_at', 'updated_at', 'group', 'status'
        )
        read_only_fields = ('uuid',)
        extra_kwargs = {
            'group': {'write_only': True},
        }
