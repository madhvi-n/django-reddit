from rest_framework import serializers
from reports.models import PostReport


class PostReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReport
        fields = (
            'id', 'reporter', 'report_type', 'url', 'post',
            'additional_info', 'status',
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            'post': {'write_only': True}
        }

    def create(self, validated_data):
        report = PostReport.objects.create(**validated_data)
        return report


class PostReportLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReport
        fields = (
            'id', 'status'
        )
        read_only_fields = ('id', 'status')
