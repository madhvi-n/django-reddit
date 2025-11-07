from core.serializers import ModelReadOnlySerializer
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "date_joined",
        )


class UserReadOnlySerializer(ModelReadOnlySerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "username")
