from reports.models import ReportType
from rest_framework import serializers


class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportType
        fields = ("id", "title", "info")
        read_only_fields = ("id",)
