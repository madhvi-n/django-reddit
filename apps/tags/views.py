from django.shortcuts import render
from .models import Tag
from core.views import BaseViewSet
from .serializers import TagSerializer


class TagViewSet(BaseViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # def get_queryset(self):
    #     name = self.request.query_params.get('search_text', None)
    #     type = self.request.query_params.get('type', None)
    #     project = self.request.query_params.get('project', None)
    #     publication = self.request.query_params.get('publication', None)
    #     queryset = self.queryset
    #
    #     if name is not None or type is not None:
    #         if type is None:
    #             queryset = self.queryset.filter(Q(name__icontains=name)).distinct().order_by('-updated_at')[:5]
    #         elif name is None:
    #             queryset = self.queryset.filter(tag_type__type=type).distinct()
    #         else:
    #             queryset = self.queryset.filter(Q(tag_type__type=type) & (Q(name__icontains=name) )).distinct().order_by('-updated_at')[:5]
    #
    #     if project:
    #         queryset = self.queryset.exclude(project_tag_sets=None)
    #     if publication:
    #         queryset = self.queryset.exclude(publications=None)
    #     return queryset
