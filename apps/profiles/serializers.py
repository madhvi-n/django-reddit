from django.contrib.auth.models import User
from rest_framework import serializers
from core.serializers import ModelReadOnlySerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'date_joined',)


class UserReadOnlySerializer(ModelReadOnlySerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')
