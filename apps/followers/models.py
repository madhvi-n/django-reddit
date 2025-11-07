from comments.models import PostComment
from django.contrib.auth.models import User
from django.db import models
from followers.abstracts import AbstractFollower
from posts.models import Post


class PostFollower(AbstractFollower):
    post = models.ForeignKey(
        Post, verbose_name="post", on_delete=models.CASCADE, related_name="followers"
    )

    class Meta:
        ordering = [
            "-created_at",
        ]
        verbose_name = "Post Follower"
        verbose_name_plural = "Post Followers"

    def __str__(self):
        return f"{self.follower.username} started following {self.post.title}"


class UserFollower(AbstractFollower):
    followed_user = models.ForeignKey(
        User,
        verbose_name="followed_user",
        on_delete=models.CASCADE,
        related_name="followers",
    )

    class Meta:
        ordering = [
            "-created_at",
        ]
        verbose_name = "User Follower"
        verbose_name_plural = "User Followers"

    def __str__(self):
        return (
            f"{self.follower.username} started following {self.followed_user.username}"
        )
