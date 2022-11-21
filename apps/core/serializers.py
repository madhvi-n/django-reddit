from django.db.models.query import QuerySet
from rest_framework import serializers
from django.apps import apps
import re


class ModelReadOnlySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ModelReadOnlySerializer, self).__init__(*args, **kwargs)

        meta = getattr(self, 'Meta')
        meta.read_only_fields = meta.fields

    class Meta:
        read_only_fields = ('id',)
    pass
