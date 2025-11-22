import django_filters
from tags.models import Tag


class TagFilterSet(django_filters.rest_framework.FilterSet):
    tag_type__title = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Tag
        fields = ("name", "tag_type")
