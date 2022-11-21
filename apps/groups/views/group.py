from rest_framework import viewsets, generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from core.views import BaseViewSet, BaseReadOnlyViewSet
from groups.models import Group
from django.contrib.auth.models import User
from groups.filters import GroupFilterSet
from groups.serializers import GroupReadOnlySerializer, GroupSerializer, GroupCreateSerializer, GroupHeavySerializer
from posts.models import Post
from posts.serializers import PostReadOnlySerializer


class GroupPagination(PageNumberPagination):
    page_size = 24


class GroupViewSet(BaseReadOnlyViewSet):
    queryset = Group.objects.all().order_by('created_at')
    serializer_class = GroupReadOnlySerializer
    permission_classes = [IsAuthenticated, ]
    filterset_class = GroupFilterSet
    serializer_action_classes = {
        'retrieve' : GroupHeavySerializer,
        'posts': PostReadOnlySerializer
    }

    @action(detail=True)
    def get_posts(self, request, pk=None):
        group = self.get_object()
        queryset = Post.objects.filter(group=group)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupSelfViewSet(BaseViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupReadOnlySerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [filters.SearchFilter,]
    search_fields = ['name', 'description']
    filterset_class = GroupFilterSet
    serializer_action_classes = {
        'create' : GroupCreateSerializer,
        'update' : GroupCreateSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(members__user=user)
        return queryset

    def create(self, request):
        data = request.data
        if not request.user.is_authenticated:
            return Response({
                'error':'The user is anonymous'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data, context={'user': request.user })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

    @action(detail=True)
    def change_type(self, request, pk=None):
        pass
