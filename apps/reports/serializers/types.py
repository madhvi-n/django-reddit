from rest_framework import serializers
from reports.models import ReportType


class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportType
        fields = ('id', 'title', 'info')
        read_only_fields = ('id',)
