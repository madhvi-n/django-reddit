from rest_framework import viewsets, generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from core.views import BaseViewSet, BaseReadOnlyViewSet
from groups.models import MemberRequest
from django.contrib.auth.models import User
from groups.serializers import MemberRequestSerializer
from groups.models import Group


class MemberRequestPagination(PageNumberPagination):
    page_size = 24


class MemberRequestViewSet(BaseViewSet):
    queryset = MemberRequest.objects.all()
    serializer_class = MemberRequestSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = self.queryset
        if self.kwargs != {}:
            if 'group_pk' in self.kwargs:
                return self.queryset.filter(group__pk=self.kwargs['group_pk'])
        return queryset

    def create(self, request, group_pk=None):
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
        if group_pk is not None:
            try:
                data['group'] = Group.objects.get(pk=group_pk).pk
            except Group.DoesNotExist:
                return Response(
                    {'error': 'Group does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'error': 'Error in route'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data, context={'request': request})
        if (serializer.is_valid(raise_exception=False)):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, post_uuid=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, post_uuid=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, group_pk=None, pk=None):
        member_request = self.get_object()
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Unauthorized user'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if member_request.user.pk != request.user.pk:
            return Response(
                {'error': 'Spoofing detected'},
                status=status.HTTP_403_FORBIDDEN
            )
        member_request.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
