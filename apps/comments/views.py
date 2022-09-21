from django.db import models
from django.db.models import Q, F, Prefetch, Min, Max, Case, When, OuterRef, Subquery
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.views import BaseReadOnlyViewSet, BaseViewSet

from posts.models import Post
from comments.models import PostComment

from comments.serializers import PostCommentSerializer, PostCommentCreateSerializer

from comments.services import add_mentioned_users


class PostCommentPagination(PageNumberPagination):
    page_size = 20


class PostCommentViewSet(BaseViewSet):
    queryset = PostComment.objects.all()
    pagination_class = PostCommentPagination
    serializer_class = PostCommentSerializer
    serializer_action_classes = {
        'list' : PostCommentSerializer,
        'create' : PostCommentCreateSerializer,
        'update' : PostCommentCreateSerializer,
    }

    def get_queryset(self):
        queryset = self.queryset.filter(is_removed=True)
        if self.kwargs != {}:
            if 'post_uuid' in self.kwargs:
                return self.queryset.filter(post__uuid=self.kwargs['post_uuid'])
        return queryset

    def list(self, request, post_uuid=None):
        deleted_with_children = PostComment.objects\
            .filter(
                parent=None,
                post__uuid=post_uuid,
                is_removed=True)\
            .exclude(comments=None).distinct()
        queryset = self.get_queryset().filter(parent=None, is_removed=False).distinct()
        queryset = queryset | deleted_with_children
        return self.paginated_response(queryset)

    def create(self, request, post_uuid=None):
        data = request.data
        mentioned_users = data.pop('mentioned_users', None)

        if not request.user.is_authenticated:
            return Response(
                {'error': 'User not authorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if data['user'] != request.user.pk:
            return Response(
                {'error': 'spoofing detected'},
                status=status.HTTP_403_FORBIDDEN
            )
        if post_uuid is not None:
            try:
                data['post'] = Post.objects.get(uuid=post_uuid).pk
            except Post.DoesNotExist:
                return Response({'error': 'Wrong UUID'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Error in route'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            comment = serializer.save()
            if mentioned_users is not None:
                for user in mentioned_users:
                    comment = add_mentioned_users(user, comment)
            serializer = PostCommentSerializer(instance=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, post_uuid=None, pk=None):
        data = request.data
        comment = self.get_object()

        if not request.user.is_authenticated:
            return Response({'error': 'The user is anonymous'}, status=status.HTTP_401_UNAUTHORIZED)
        if data['user'] != request.user.pk:
            return Response({'error': 'spoofing detected'}, status=status.HTTP_403_FORBIDDEN)

        if post_uuid is not None:
            try:
                data['post'] = Post.objects.get(uuid=post_uuid).pk
            except Post.DoesNotExist:
                return Response({'error': 'Wrong UUID'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Error in route'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data,instance=comment)
        if serializer.is_valid():
            comment = serializer.save()
            serializer = PostCommentSerializer(instance=comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, post_uuid=None):
        comment = self.get_object()
        user = request.user
        if comment.user != user:
            return Response (
                {'error' : 'User not authorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        comment.is_removed = True
        comment.save()
        return Response({'success': True}, status=status.HTTP_200_OK)

    # @action(detail=False)
    # def user_comments(self, request, pk=None, post_uuid=None):
    #     queryset = self.get_queryset().filter(Q(user=request.user) | Q(mentioned_users=request.user))
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response(serializer.data)

    @action(detail=True)
    def children(self, request, post_uuid=None, pk=None):
        comment = self.get_object()
        children_comments = PostComment.objects.filter(parent=comment)
        deleted_with_children = children_comments.filter(is_removed=True)\
            .exclude(comments=None).distinct()
        queryset = children_comments.filter(is_removed=False).distinct()
        queryset = queryset | deleted_with_children
        return self.paginated_response(queryset)
