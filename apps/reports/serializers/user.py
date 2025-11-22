from reports.models import UserProfileReport
from rest_framework import serializers


class UserProfileReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileReport
        fields = (
            "id",
            "reporter",
            "report_type",
            "url",
            "reported_user",
            "additional_info",
            "status",
        )
        read_only_fields = ("id",)
        extra_kwargs = {"reported_user": {"write_only": True}}

    def create(self, validated_data):
        report = UserProfileReport.objects.create(**validated_data)
        return report


class UserProfileReportLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileReport
        fields = ("id", "status")
        read_only_fields = ("id", "status")
