from django.db.models.query import EmptyQuerySet, QuerySet

from rest_framework import serializers

from django.apps import apps
from core.services import camel_to_snake

import serpy
import re


class ModelReadOnlySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ModelReadOnlySerializer, self).__init__(*args, **kwargs)

        meta = getattr(self, 'Meta')
        meta.read_only_fields = meta.fields

    class Meta:
        read_only_fields = ('id',)
    pass


class BaseReadOnlySerializer(serializers.BaseSerializer):
    """
    A read-only serializer that coerces arbitrary complex objects
    into primitive representations.
    NOTE: Meta class is compulsory
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(BaseReadOnlySerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            meta = getattr(self, 'Meta')
            allowed = set(fields)
            existing = set(meta.fields)
            meta.fields = existing - (existing - allowed)
            # meta.fields.pop(field_name)

    def to_representation(self, instance):
        output = {}
        meta = getattr(self, 'Meta')
        # import pdb; pdb.set_trace()

        display_fields = meta.fields if hasattr(meta, 'fields') else ()
        flat = meta.flat if hasattr(meta, 'flat') else False

        for display_field in display_fields:
            try:
                field = instance._meta.get_field(display_field)
            except Exception:
                field = instance._meta.get_field('id')

            many = field.many_to_many or field.one_to_many

            if display_field.startswith('_'):
                # Ignore private attributes even if in display.
                continue

            program = 'global attribute; attribute = instance.' \
                + display_field \
                + ('.all()' if many else '')
            exec(program)
            # import pdb; pdb.set_trace

            if hasattr(attribute, '__call__'):
                # Ignore methods and other callables.
                continue
            # elif not field.concrete:
            #     # Ignore if column does not exist
            #     continue
            # elif field.is_relation:
            #     pass
            elif isinstance(attribute, (str, int, bool, float, type(None))):
                # Primitive types can be passed through unmodified.
                output[display_field] = attribute

            elif isinstance(attribute, dict):
                # Recursively deal with items in dictionaries.
                output[display_field] = {
                    str(key): self.to_representation(value)
                    for key, value in attribute.items()
                }
            elif field.is_relation \
                    and not flat \
                    and display_field in meta.serializer_fields.keys():

                related_serializer = meta.serializer_fields[display_field]
                output[display_field] = related_serializer(
                    attribute, many=many).data
            elif isinstance(attribute, list) \
                    or isinstance(attribute, QuerySet):
                # Recursively deal with items in lists.
                output[display_field] = [
                    str(item) for item in attribute
                ]
            else:
                # Force anything else to its string representation.
                output[display_field] = str(attribute)
        return output
