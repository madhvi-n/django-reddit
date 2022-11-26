import django_filters
from posts.models import Post


class PostFilterSet(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Post
        fields = ('title', 'status', 'group', 'author')
