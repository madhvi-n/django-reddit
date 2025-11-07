from core.views import BaseReadOnlyViewSet, BaseViewSet
from django.contrib.auth.models import User
from groups.filters import GroupFilterSet
from groups.models import Group, GroupMember, MemberRequest
from groups.permissions import HasGroupDeletePermissions, HasGroupEditPermissions
from groups.serializers import (
    GroupCreateSerializer,
    GroupHeavySerializer,
    GroupReadOnlySerializer,
    GroupSerializer,
)
from posts.models import Post
from posts.serializers import PostReadOnlySerializer
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class GroupPagination(PageNumberPagination):
    page_size = 24


class GroupViewSet(BaseViewSet):
    queryset = Group.objects.all().order_by("created_at")
    serializer_class = GroupSerializer
    serializer_action_classes = {
        "create": GroupCreateSerializer,
        "update": GroupCreateSerializer,
        "retrieve": GroupHeavySerializer,
        "posts": PostReadOnlySerializer,
    }
    permission_action_classes = {
        "update": [
            HasGroupEditPermissions,
        ],
        "destroy": [
            HasGroupDeletePermissions,
        ],
        "add_topic": [HasGroupEditPermissions],
        "remove_topic": [HasGroupEditPermissions],
    }
    pagination_class = GroupPagination
    filterset_class = GroupFilterSet

    def list(self, request):
        queryset = self.queryset
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        group = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(group, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        if not request.user.is_authenticated:
            return Response(
                {"error": "The user is anonymous"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        data = request.data
        if not request.user.is_authenticated:
            return Response(
                {"error": "The user is anonymous"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True)
    def posts(self, request, pk=None):
        group = self.get_object()
        queryset = Post.objects.filter(group=group)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            queryset, many=True, context={"user": request.user}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True)
    def add_topic(self, request, pk=None):
        return Response(status=status.HTTP_200_OK)

    @action(detail=True)
    def remove_topic(self, request, pk=None):
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["put"])
    def leave_group(self, request, pk=None):
        group = self.get_object()
        data = request.data
        if not request.user.is_authenticated:
            return Response(
                {"error": "The user is anonymous"}, status=status.HTTP_401_UNAUTHORIZED
            )
        if data["user"] != request.user.pk:
            return Response(
                {"error": "Spoofing detected"}, status=status.HTTP_403_FORBIDDEN
            )
        try:
            request = MemberRequest.objects.filter(id=data["member_request"]).first()
            request.delete()
            member = GroupMember.objects.filter(group=group, user=request.user).first()
            member.delete()
        except MemberRequest.DoesNotExist:
            return Response(
                {"error": "Member request does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except GroupMember.DoesNotExist:
            return Response(
                {"error": "Group Member does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"success": True}, status=status.HTTP_200_OK)
