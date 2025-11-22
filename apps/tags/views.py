from core.views import BaseViewSet
from django.shortcuts import render

from .filters import TagFilterSet
from .models import Tag
from .serializers import TagSerializer


class TagViewSet(BaseViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filterset_class = TagFilterSet
    ordering = ["-created_at"]
