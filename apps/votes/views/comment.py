from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.views import BaseViewSet
from comments.models import PostComment
from votes.serializers import PostCommentVoteSerializer
from votes.models import PostCommentVote


class PostCommentVotePagination(PageNumberPagination):
    page_size = 24


class PostCommentVoteViewSet(BaseViewSet):
    queryset = PostCommentVote.objects.all()
    pagination_class = PostCommentVotePagination
    serializer_class = PostCommentVoteSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.kwargs != {}:
            if 'comment_pk' in self.kwargs:
                return self.queryset.filter(comment__pk=self.kwargs['comment_pk'])
        return queryset

    def list(self, request, comment_pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, comment_pk=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, comment_pk=None):
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
        if comment_pk is not None:
            try:
                data['comment'] = PostComment.objects.get(pk=comment_pk).pk
            except PostComment.DoesNotExist:
                return Response(
                    {'error': 'PostComment does not exist'},
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

    def update(self, request, comment_pk=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, comment_pk=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, comment_pk=None, pk=None):
        comment = self.get_object()
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Unauthorized user'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if comment.user.pk != request.user.pk:
            return Response(
                {'error': 'Spoofing detected'},
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
