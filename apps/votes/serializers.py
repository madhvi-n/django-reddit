from rest_framework import serializers
from votes.models import PostVote, PostCommentVote


class PostVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVote
        fields = ('id', 'post', 'user', 'vote')
        read_only_fields = ('id',)
        extra_kwargs = {
            'post': {'write_only': True}
        }

    def create(self, validated_data):
        return PostVote.objects.create(**validated_data)


class PostVoteLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVote
        fields = ('id', 'user', 'vote')
        read_only_fields = ('id',)


class PostCommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentVote
        fields = ('id', 'post_comment', 'user')
        read_only_fields = ('id',)
        extra_kwargs = {
            'post_comment': {'write_only': True}
        }

    def create(self, validated_data):
        return PostCommentVote.objects.create(**validated_data)


class PostCommentVoteLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentVote
        fields = ('id', 'user')
        read_only_fields = ('id',)
