from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.views import BaseReadOnlyViewSet, BaseViewSet
from followers.models import PostFollower, UserFollower
from posts.models import Post
from django.contrib.auth.models import User
from followers.serializers import PostFollowerSerializer, UserFollowerSerializer


class PostFollowerPagination(PageNumberPagination):
    page_size = 24


class PostFollowerViewSet(BaseViewSet):
    queryset = PostFollower.objects.all()
    pagination_class = PostFollowerPagination
    serializer_class = PostFollowerSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.kwargs != {}:
            if 'post_uuid' in self.kwargs:
                return self.queryset.filter(post__uuid=self.kwargs['post_uuid'])
        return queryset

    def list(self, request, post_uuid=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, post_uuid=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, post_uuid=None):
        data = request.data
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Unauthorized user'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if data['follower'] != request.user.pk:
            return Response(
                {'error': 'Spoofing detected'},
                status=status.HTTP_403_FORBIDDEN
            )
        if post_uuid is not None:
            try:
                data['post'] = Post.objects.get(uuid=post_uuid).pk
            except Post.DoesNotExist:
                return Response(
                    {'error': 'Post does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'error': 'Error in route'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        if (serializer.is_valid(raise_exception=False)):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, post_uuid=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, post_uuid=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, post_uuid=None, pk=None):
        post_follower = self.get_object()
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Unauthorized user'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if post_follower.follower.pk != request.user.pk:
            return Response(
                {'error': 'Spoofing detected'},
                status=status.HTTP_403_FORBIDDEN
            )
        post_follower.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class UserFollowerPagination(PageNumberPagination):
    page_size = 24


class UserFollowerViewSet(BaseViewSet):
    queryset = UserFollower.objects.all()
    pagination_class = UserFollowerPagination
    serializer_class = UserFollowerSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.kwargs != {}:
            if 'user_username' in self.kwargs:
                return self.queryset.filter(followed_user__username=self.kwargs['user_username'])
        return queryset

    def list(self, request, user_username=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, user_username=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, user_username=None):
        data = request.data
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Unauthorized user'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if data['follower'] != request.user.pk:
            return Response(
                {'error': 'Spoofing detected'},
                status=status.HTTP_403_FORBIDDEN
            )
        if user_username is not None:
            try:
                data['followed_user'] = User.objects.get(username=user_username).pk
            except User.DoesNotExist:
                return Response(
                    {'error': 'User profile does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'error': 'Error in route'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        if (serializer.is_valid(raise_exception=False)):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, user_username=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, user_username=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, user_username=None, pk=None):
        user_follower = self.get_object()
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Unauthorized user'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if user_follower.follower.pk != request.user.pk:
            return Response(
                {'error': 'Spoofing detected'},
                status=status.HTTP_403_FORBIDDEN
            )
        user_follower.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
