from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.views import BaseViewSet
from posts.models import Post
from votes.serializers import PostVoteSerializer
from votes.models import PostVote


class PostVotePagination(PageNumberPagination):
    page_size = 24


class PostVoteViewSet(BaseViewSet):
    queryset = PostVote.objects.all()
    pagination_class = PostVotePagination
    serializer_class = PostVoteSerializer

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
        if data['user'] != request.user.pk:
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
        post = self.get_object()
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Unauthorized user'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if post.user.pk != request.user.pk:
            return Response(
                {'error': 'Spoofing detected'},
                status=status.HTTP_403_FORBIDDEN
            )
        post.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
