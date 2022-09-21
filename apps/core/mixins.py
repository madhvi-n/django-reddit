from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.
        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()


class MultiPermissionViewSetMixin(object):
    def get_permissions(self):
        """
        Look for permission class in self.permission_action_classes, which
        should be a dict mapping action name (key) to permission class (value),
        i.e.:

        class MyViewSet(MultiPermissionViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            permission_action_classes = {
                'create': [NotAuthenticated],
                'confirm_email': [NotAuthenticated],
                'update': [IsAuthenticated],
                'retrieve': [AllowAny],
                'partial_update': [IsAuthenticated],
            }

            @action
            def my_action:
                ...

                If there's no entry for that action then just fallback to the regular
                get_permissions lookup: self.permission_classes, DefaultPermissions.
                """
        try:
            permissions = self.permission_action_classes[self.action]
            return [permission() for permission in permissions]
        except (KeyError, AttributeError):
            return super(MultiPermissionViewSetMixin, self).get_permissions()


class PaginatedResponseMixin(object):
    def paginated_response(self, queryset, context=None, paginator=None, fields=None):
        """
        This function should be called when a paginated response is needed
        """
        page = None

        if paginator is not None:
            page = paginator.paginate_queryset(queryset, request=self.request)
        else:
            page = self.paginate_queryset(queryset)

        if page is not None:
            kwargs = {}
            if fields is not None:
                kwargs = {'fields': fields}
            serializer = self.get_serializer(page, context=context, many=True, **kwargs)
            if paginator is not None:
                return paginator.get_paginated_response(serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, context=context, many=True, fields=fields)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DestroyModelMixin:
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': True }, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
