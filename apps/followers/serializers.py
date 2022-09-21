from rest_framework import serializers

from followers.models import PostFollower, UserFollower


class PostFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFollower
        fields = ('id', 'post', 'follower')
        read_only_fields = ('id',)
        extra_kwargs = {
            'post': {'write_only': True}
        }

    def create(self, validated_data):
        return PostFollower.objects.create(**validated_data)


class UserFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollower
        fields = ('id', 'followed_user', 'follower')
        read_only_fields = ('id',)
        extra_kwargs = {
            'followed_user': {'write_only': True}
        }

    def create(self, validated_data):
        return UserFollower.objects.create(**validated_data)
