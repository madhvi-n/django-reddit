from posts.models import Post, PostVote
from core.views import BaseViewSet, BaseReadOnlyViewSet
from posts.serializers import PostSerializer, PostEditSerializer
from rest_framework import viewsets, generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from comments.serializers import PostCommentCreateSerializer, PostCommentSerializer
from django.contrib.auth.models import User
from posts.filters import PostFilterSet


class PostPagination(PageNumberPagination):
    page_size = 12


class PostViewSet(BaseReadOnlyViewSet):
    queryset = Post.objects.all().exclude(status=Post.STATUS.DRAFT)
    serializer_class = PostSerializer
    pagination_class = PostPagination
    lookup_field = 'uuid'
    filterset_class = PostFilterSet

    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        context.update({'source': 'Post'})
        return context

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return self.paginated_response(queryset, context={'request': request})

    def retrieve(self, request, uuid=None):
        post = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _common_vote_method(self, request, method):
        post = self.get_object()
        user = request.user
        vote, created = PostVote.objects.get_or_create(post=post, user=user)
        if method == "upvote":
            vote.vote = 1
        elif method == "downvote":
            vote.vote = -1
        else:
            vote.vote = 0
        vote.save()
        return Response({"vote": vote.vote, "votes": post.score}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def upvote(self, request, uuid=None):
        return self._common_vote_method(request, "upvote")

    @action(detail=True, methods=['put'])
    def downvote(self, request, uuid=None):
        return self._common_vote_method(request, "downvote")

    @action(detail=True, methods=['put'])
    def remove_vote(self, request, uuid=None):
        return self._common_vote_method(request, "remove_vote")


class PostSelfViewSet(BaseViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    lookup_field = 'uuid'
    serializer_class = PostEditSerializer
    pagination_class = PostPagination
    filterset_class = PostFilterSet
    permission_classes = [IsAuthenticated, ]
    serializer_action_classes = {
        'list' : PostSerializer,
        'create' : PostEditSerializer,
        'update' : PostEditSerializer,
        'drafts' : PostSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(author=user)
        return queryset

    def create(self, request):
        data = request.data
        if not request.user.is_authenticated:
            return Response({'error':'The user is anonymous'}, status=status.HTTP_401_UNAUTHORIZED)
        if data['author'] != request.user.pk:
            return Response({'error': 'Spoofing detected'}, status=status.HTTP_403_FORBIDDEN)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, uuid=None):
        post = self.get_object()
        data = request.data
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "User not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if post.author != user:
            return Response({"error": "Spoofing detected"}, status=status.HTTP_403_FORBIDDEN)

        post.title = data['title']
        post.content = data['content']
        post.save()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data, instance=post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, uuid=None):
        post = self.get_object()
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if post.author != user:
            return Response({"error": "Spoofing detected"}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)

    def add_tag(self, request, uuid=None):
        post = self.get_object()
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if post.author != user:
            return Response({"error": "Spoofing detected"}, status=status.HTTP_403_FORBIDDEN)
        try:
            tag = data.pop('tag', None)
            tag_obj = None
            if 'id' in tag.keys():
                tag_obj = Tag.objects.get(pk=tag['id'])
            else:
                tag_obj, created = Tag.objects.get_or_create(name=tag['name'])
            if tag_obj is not None and tag_obj not in post.tags.all():
                post.tags.add(tag_obj)
        except Exception as e:
            return Response({"error": str(e), "message": e.message}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(tag_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def remove_tag(self, request, uuid=None):
        post = self.get_object()
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if post.author != user:
            return Response({"error": "Spoofing detected"}, status=status.HTTP_403_FORBIDDEN)
        try:
            tag = data.pop('tag', None)
            tag_obj = None
            if 'id' in tag.keys():
                tag_obj = Tag.objects.get(pk=tag['id'])
            if tag_obj is not None and tag_obj in post.tags.all():
                post.tags.remove(tag_obj)
        except Exception as e:
            return Response({"error": str(e), "message": e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': True}, status=status.HTTP_200_OK)

    def archive(self, request, uuid=None):
        post = self.get_object()
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if post.author != user:
            return Response({"error": "Spoofing detected"}, status=status.HTTP_403_FORBIDDEN)
        post.status = Post.STATUS.ARCHIVED
        post.save()
        return Response({'success': True}, status=status.HTTP_200_OK)

    def save_draft(self, request, uuid=None):
        post = self.get_object()
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if post.author != user:
            return Response({"error": "Spoofing detected"}, status=status.HTTP_403_FORBIDDEN)
        post.status = Post.STATUS.DRAFT.value
        post.save()
        return Response({'success': True}, status=status.HTTP_200_OK)
