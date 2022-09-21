from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .mixins import (
    MultiSerializerViewSetMixin,
    MultiPermissionViewSetMixin,
    PaginatedResponseMixin,
    DestroyModelMixin,
)

class BaseReadOnlyViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        MultiSerializerViewSetMixin,
        MultiPermissionViewSetMixin,
        PaginatedResponseMixin,
        viewsets.GenericViewSet):

    def get_serializer_context(self):
        context = super(BaseReadOnlyViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BaseViewSet(
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        DestroyModelMixin,
        BaseReadOnlyViewSet):
    pass
