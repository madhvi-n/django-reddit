import django_filters
from django.db import models
from posts.models import Post


class PostFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="contains")
    author = django_filters.CharFilter(
        field_name="author__username", lookup_expr="exact"
    )

    class Meta:
        model = Post
        fields = ("title", "status", "group", "author")
