from rest_framework import serializers
from posts.models import Post
from profiles.serializers import UserSerializer
from tags.serializers import TagSerializer
from comments.models import PostComment
from votes.serializers import PostVoteLightSerializer, PostCommentVoteLightSerializer
from votes.models import PostVote
from bookmarks.models import PostBookmark
from bookmarks.serializers import PostBookmarkLightSerializer
from django.db.models import Sum

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    votes = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    user_bookmark = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    tags = TagSerializer(required=False, many=True)

    class Meta:
        model = Post
        fields = (
            'title', 'content', 'uuid', 'author', 'votes',
            'comments', 'created_at', 'updated_at', 'tags',
            'user_vote', 'user_bookmark'
        )

    def get_votes(self, obj):
        if obj.votes.exists():
            post = obj.votes.aggregate(votes=Sum('vote'))
            return post['votes']
        return 0

    def get_comments(self, obj):
        return PostComment.objects.filter(post=obj, is_removed=False).count()

    def get_user_vote(self, obj):
        request = self.context.get('request', None)
        if request is not None and request.user.is_authenticated:
            votes = PostVote.objects.filter(post=obj, user=request.user)\
                .order_by('-updated_at')
            if votes.exists():
                return PostVoteLightSerializer(votes.first()).data
        return None

    def get_user_bookmark(self, obj):
        request = self.context.get('request', None)
        if request is not None and request.user.is_authenticated:
            bookmarks = PostBookmark.objects.filter(post=obj, user=request.user)\
            .order_by('-updated_at')
            if bookmarks.exists():
                return PostBookmarkLightSerializer(bookmarks.first()).data
        return None


class PostEditSerializer(serializers.ModelSerializer):
    tags = TagSerializer(required=False, many=True)

    class Meta:
        model = Post
        fields = (
            'uuid', 'title', 'content', 'author', 'tags',
            'created_at', 'updated_at'
        )
        read_only_fields = ('uuid',)
